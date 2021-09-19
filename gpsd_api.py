import socket
import json
from threading import Lock


class Connection:
    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect(('localhost', 2947))
        self._s.setblocking(False)
        self._server_info = self._get(no_wait=False)[0]
        #TODO: any validation needed here?

        self._queue = []
        self._lock = Lock()
        self._enabled = False

    def _get(self, no_wait=True):
        data = b''
        while True:
            try:
                data += self._s.recv(1024)
            except BlockingIOError:
                if no_wait or data.endswith(b'\r\n'):
                    break
        lines = [ json.loads(i) for i in data.split(b'\r\n')[:-1] ]
        return lines

    def get_messages(self, accept_classes='all', required_keys={'TPV': ['lat', 'lon']}, clear=False):
        with self._lock:
            messages = self._queue + self._get()

            if accept_classes == 'all':
                self._queue = []
                return messages
            elif accept_classes == 'none':
                self._queue = [] if clear else messages
                return []
            else:
                out = []
                requeue = []

                for message in messages:
                    accept = False
                    if message['class'] in accept_classes:
                        try:
                            rk = required_keys[message['class']]
                        except KeyError:
                            rk = []
                        accept = all([i in message.keys() for i in rk])

                    if accept:
                        out.append(message)
                    else:
                        requeue.append(message)

                self._queue = [] if clear else requeue
                return out

    def clear_queue(self):
        with self._lock:
            self._queue = []

    @property
    def server_info(self):
        with self._lock:
            return self._server_info

    def _set_enabled(self, enabled):
        if not isinstance(enabled, bool):
            raise ValueError('enabled attribute of Connection must be a bool')

        with self._lock:
            self._s.sendall(b'?WATCH={"enable":true,"json":true}' if enabled else b'?WATCH{"enable":false}')
            self._enabled = enabled

    def _get_enabled(self):
        with self._lock:
            return self._enabled

    enabled = property(_get_enabled, _set_enabled)
