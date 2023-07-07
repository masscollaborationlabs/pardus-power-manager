#!/usr/bin/env python3
import gi, os, sys, subprocess
gi.require_version('Gtk', '3.0')

# FIXME: remove this
def _(msg):
    return msg

from gi.repository import GLib, Gtk
sys.path.insert(0, os.path.dirname( os.path.realpath(__file__) )+"/../common")
from common import *

def fint(ctx):
    ret = ""
    for c in ctx:
        if c in "0123456789":
            ret += c
    return int(ret)


class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../data/MainWindow.ui")
        self.window = self.builder.get_object("ui_window_main")
        self.connect_signals()
        self.combobox_init()
        self.spinbutton_init()
        self.value_init()

    def combobox_init(self):
        store = Gtk.ListStore(str, str)
        store.append([_("Performance"),"performance"])
        store.append([_("Powersave"),"powersave"])
        store.append([_("Ignore"),"ignore"])
        self.o("ui_combobox_acmode").set_model(store)
        self.o("ui_combobox_batmode").set_model(store)
        cellrenderertext = Gtk.CellRendererText()
        self.o("ui_combobox_acmode").pack_start(cellrenderertext, True)
        self.o("ui_combobox_acmode").add_attribute(cellrenderertext, "text", 0)
        self.o("ui_combobox_batmode").pack_start(cellrenderertext, True)
        self.o("ui_combobox_batmode").add_attribute(cellrenderertext, "text", 0)

    def spinbutton_init(self):
        self.o("ui_spinbutton_powersave").set_range(0,100)
        self.o("ui_spinbutton_performance").set_range(0,100)
        self.o("ui_spinbutton_powersave").set_increments(1,1)
        self.o("ui_spinbutton_performance").set_increments(1,1)
        self.o("ui_spinbutton_powersave").set_digits(0)
        self.o("ui_spinbutton_performance").set_digits(0)


    def value_init(self):
        self.o("ui_switch_service").set_state(get("enabed",True,"service"))
        self.o("ui_switch_gpu").set_state(get("disable-3d-controller",False,"service"))
        self.o("ui_spinbutton_powersave").set_value(fint(get("backlight-powersave","%50","modes")))
        self.o("ui_spinbutton_performance").set_value(fint(get("backlight-performance","%100","modes")))
        l = ["performance", "powersave", "ignore"]
        self.o("ui_combobox_acmode").set_active(l.index(get("ac-mode","performance","modes")))
        self.o("ui_combobox_batmode").set_active(l.index(get("bat-mode","powersave","modes")))


    def connect_signals(self):
        self.window.connect("destroy",Gtk.main_quit)
        self.o("ui_button_cancel").connect("clicked",Gtk.main_quit)
        self.o("ui_button_save").connect("clicked",self.save_settings)

    def o(self,name):
        return self.builder.get_object(name)

    def save_settings(self, widget):
        data = {}
        # service
        data["service"] = {}
        data["service"]["enabled"] = self.o("ui_switch_service").get_state()
        data["service"]["disable-3d-controller"] = self.o("ui_switch_gpu").get_state()
        # modes
        data["modes"] = {}
        ac_w = self.o("ui_combobox_acmode")
        bat_w = self.o("ui_combobox_batmode")
        t = ac_w.get_active_iter()
        print(t)
        data["modes"]["ac-mode"] = ac_w.get_model()[t][1]
        t = bat_w.get_active_iter()
        data["modes"]["bat-mode"] = bat_w.get_model()[t][1]
        # backlight
        data["modes"]["backlight-powersave"] = "%"+str(int(self.o("ui_spinbutton_powersave").get_value()))
        data["modes"]["backlight-performance"] = "%"+str(int(self.o("ui_spinbutton_performance").get_value()))
        print(data)

if __name__ == "__main__":
    if os.getuid() != 0 and "--test" not in sys.argv:
        subprocess.run(["pkexec", "/usr/share/pardus/power-manager/settings/main.py"])
        exit(0)
    main = MainWindow()
    main.window.show()
    Gtk.main()
