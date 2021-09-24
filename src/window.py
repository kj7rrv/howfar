import gi
gi.require_version('Handy', '1')
from gi.repository import Gtk, Handy


@Gtk.Template(resource_path='/com/github/linux-distance-tracker/window.ui')
class LdtWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'LdtWindow'
    Handy.init()

    # label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
