#Main entrance for GUI
import PySimpleGUI as sg
import os, sys
from pathlib import Path

sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent))

from GUI import new_trip_gui
from GUI import trip_viewer_gui

__version__ = "alpha"
logo_path = os.path.join(os.path.abspath(__file__),"..", "logo.png")
TNR = "Times New Roman"
THEME = "DefaultNoMoreNagging"

print(logo_path)

keybind_maps = {
    "<Control_R><w>":"control-w", "<Control_L><w>":"control-w", "<Control_R><W>":"control-w", "<Control_L><W>":"control-w",
    "<Control_R><n>":"control-n", "<Control_L><n>":"control-n", "<Control_R><N>":"control-n", "<Control_L><N>":"control-n"
}

def bindkey(window, map):
    if not isinstance(window, sg.Window):
        raise TypeError("Input window is not a GUI window object")
    for k, v in map.items():
        window.bind(k, v)

#This is the starting gui window for splitwiser

sg.theme(THEME)
menu_def = [['File', ['New       Ctrl+N::newkey', 'Open      Ctrl+O::openkey', 'Open recent::openrecentkey', '!Save       Ctrl+S::savekey', '!Save as::saveaskey', 'Exit::exitkey']],
            ['Edit', ['Copy      Ctrl+C::copykey', 'Cut         Ctrl+X::cutkey', 'Paste     Ctrl+V::pastekey', 'Undo      Ctrl+Z::undokey', 'Redo::redokey']],
            ['Help', ['About::aboutkey']] ]

new_trip_button = sg.Button("New trip", key="new_trip_button", expand_x=True, expand_y=True, font=(TNR, 20), p=20)
open_trip_button = sg.Button("Open trip", key="open_trip_button", expand_x=True, expand_y=True, font=(TNR, 20), p=20)
exit_button = sg.Button("Exit", key="exit_button", expand_x=True, expand_y=True, font=(TNR, 20), p=20)
logo_viewer = sg.Image(filename=logo_path, expand_x=True, expand_y=True)
title_text = sg.Text("Splitwiser", key="titletext", justification="center", font=(TNR, 40, "bold"), expand_x=True)

button_column = sg.Column([[new_trip_button],
                           [open_trip_button],
                           [exit_button]],
                           expand_x=True, expand_y=True, element_justification="center")

logo_column = sg.Column([[logo_viewer]], expand_x=True, expand_y=True)

layout = [[sg.Menu(menu_def, pad=(0,0), k='-MENUBAR-')],
          [title_text],
          [button_column, logo_column]]

window = sg.Window("Splitwiser", layout, resizable=True, size=(800,500), return_keyboard_events=True, finalize=True, auto_size_buttons=True, margins=(20,20))
bindkey(window, keybind_maps)
window.bind('<Configure>',"resize_event")

def main_gui_start():
    while True:
        event, values = window.read()
        print(event)
        if event in (sg.WIN_CLOSED, "Exit::exitkey", "control-w", "exit_button"):
            window.close()
            break
        elif event == "About::aboutkey":
            sg.popup("Splitwiser version %s" % __version__, title="Splitwiser about", keep_on_top=True)
        elif event in ("control-n", "new_trip_button","New       Ctrl+N::newkey"):
            window.disappear()
            new_trip_gui_obj = new_trip_gui.NewTripGui()
            new_trip_gui_obj.preproc()
            new_trip_gui_obj.create_new_trip(new_trip_gui_obj.preproc_status)
            if new_trip_gui_obj.create_success == 1:
                trip_viewer = trip_viewer_gui.TripViewer(new_trip_gui_obj.new_trip)
            window.reappear()
        elif event == "resize_event":
            window_x, window_y = window.size
            font_size = max(round(window_x / 80 * 4), round(window_y / 50 * 4))
            window["titletext"].update(font=(TNR,font_size, "bold"))

if __name__ == "__main__":
    main_gui_start()