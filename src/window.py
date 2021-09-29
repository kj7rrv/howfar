import gi
gi.require_version('Handy', '1')
from gi.repository import Gtk, Handy, GLib

from .gps.tracker import Tracker
from .conversion.metric import Metric
from .conversion.imperial import Imperial

@Gtk.Template(resource_path='/com/kj7rrv/howfar/window.ui')
class LdtWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'HowFarWindow'
    # init LibHandy so it renders properly
    Handy.init()

    # Bind to UI elements
    stats_avg_pace:Gtk.Label = Gtk.Template.Child()
    stats_distance:Gtk.Label = Gtk.Template.Child()
    stats_duration:Gtk.Label = Gtk.Template.Child()
    stats_pace:Gtk.Label = Gtk.Template.Child()
    start_button:Gtk.Button = Gtk.Template.Child()
    error_message_revealer:Gtk.Revealer = Gtk.Template.Child()
    error_message_label:Gtk.Label = Gtk.Template.Child()
    gps_status_icon:Gtk.Image = Gtk.Template.Child()
    gps_acquiring_spinner:Gtk.Spinner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracker = Tracker()
        self.tracker.on_event("acquire", self.on_gps_acquired)
        self.tracker.on_event("pace", self.on_pace_update)
        self.tracker.on_event("distance", self.on_distance_update)
        self.tracker.on_event("error", self.on_gps_error)
        self.converter = Metric()

    def render_number(self, number):
        return "{:.1f}".format(number)

    def toggle_tracking(self):
        if self.tracker.tracking:
            self.stop_tracking()
        else:
            self.start_tracking()

    def start_tracking(self):
        self.tracker.tracking = True
        self.start_button.set_label("Stop Tracking")
        GLib.idle_add(self.tracker.poll)

    def stop_tracking(self):
        self.tracker.tracking = False
        self.start_button.set_label("Start Tracking")
        self.gps_acquiring_spinner.stop()

    # GPS callbacks

    def on_gps_error(self, data):
        self.error_message_label.set_text(data)
        self.error_message_revealer.set_reveal_child(True)
        self.stop_tracking()
        self.gps_status_icon.set_from_icon_name("location-services-disabled-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
        self.gps_acquiring_spinner.stop()

    def on_gps_acquired(self, data):
        print("gps acquired", data)
        self.gps_acquiring_spinner.stop()
        self.gps_status_icon.set_from_icon_name("location-services-active-symbolic", Gtk.IconSize.LARGE_TOOLBAR)

    def on_pace_update(self, data):
        pace = self.converter.pace(data)
        self.stats_pace.set_text(self.render_number(pace))

    def on_distance_update(self, data):
        distance = self.converter.distance(data)
        self.stats_distance.set_text(self.render_number(distance))

    # GTK callbacks

    @Gtk.Template.Callback()
    def on_start_button_clicked(self, button, userdata=None):
        self.toggle_tracking()
        if not self.tracker.acquired:
            self.gps_acquiring_spinner.start()

    @Gtk.Template.Callback()
    def on_error_message_close(self, item, userdata=None):
        self.error_message_revealer.set_reveal_child(False)
