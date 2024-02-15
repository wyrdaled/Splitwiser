#This is the gui window for creating a new trip
import PySimpleGUI as sg
import sys, os
from pathlib import Path
from datetime import date, timedelta
from string import ascii_letters, digits
CHANGED = 0 #global variable to record if change has been made; 0 = no change, 1 = change
THEME = "DefaultNoMoreNagging"
keybind_maps = {
    "<Control_R><w>":"control-w", "<Control_L><w>":"control-w", "<Control_R><W>":"control-w", "<Control_L><W>":"control-w",
    "<Control_R><n>":"control-n", "<Control_L><n>":"control-n", "<Control_R><N>":"control-n", "<Control_L><N>":"control-n"
} #TODO: Create constant.py and import from there

sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent))
#sys.path.append("D:\\Coding\\Splitwiser")
from Trip import Trip

sg.theme(THEME)
def bindkey(window, map): #TODO: This method appeaers multiple places in splitwiser, should be put into utility and import
    if not isinstance(window, sg.Window):
        raise TypeError("Input window is not a GUI window object")
    for k, v in map.items():
        window.bind(k, v)

class NewTripGui(object):

    def __init__(self):
        self.path_to_save = None
        self.preproc_status = 0
        self.create_success = 0 #0 means create failed, 1 means create succeeded

    def preproc(self):
        sg.popup("Plese select a location so save your file\n", font=("Times New Roman", 12), button_justification="c")
        selected_dir = sg.popup_get_folder("Save new trip to directory", size=(30,100), title="New trip", font=("Times New Roman", 12))
        return_to_main = False
        print(selected_dir)
        print(selected_dir == "")
        print(type(selected_dir))
        while (selected_dir is None or not os.path.isdir(selected_dir)):
            ret_val = sg.popup_yes_no("No valid directory selected\n\nDo you want to exit?\n", font=("Times New Roman", 12))
            print(ret_val)
            if ret_val.lower() == "no":
                selected_dir = sg.popup_get_folder("Save new trip to directory", size=(30,100), title="New trip", font=("Times New Roman", 12))
            else:
                return_to_main = True
                break
        
        if return_to_main:
            return
        self.path_to_save = selected_dir
        self.preproc_status = 1 #preproc successful

    def create_new_trip(self, preproc_status):
        if preproc_status != 1:
            return
        
        title_text = sg.Text("Creating a new trip\n", font=("Times New Roman", 16, "bold"), justification='center', expand_x=True)

        trip_name_text = sg.Text("Trip name*", font=("Times New Roman", 12), pad=10)
        start_date_text = sg.Text("Start date (yyyy-mm-dd)*", font=("Times New Roman", 12), pad=10)
        end_date_text = sg.Text("End date (yyyy-mm-dd)", font=("Times New Roman", 12), pad=10)
        trip_length_text = sg.Text("Trip lengths (days)", font=("Times New Roman", 12), pad=10)
        destination_text = sg.Text("Destination", font=("Times New Roman", 12), pad=10)
        text_column = sg.Column([[trip_name_text], [start_date_text], [end_date_text], [trip_length_text], [destination_text]],
                                expand_x = False)

        trip_name_input = sg.Input("", key="trip_name_in", font=("Times New Roman", 12), pad=10, expand_x = True, enable_events = True)
        start_date_input = sg.Input("", key="start_date_in", font=("Times New Roman", 12), pad=10, expand_x = True, enable_events = True)
        end_date_input = sg.Input("", key="end_date_in", font=("Times New Roman", 12), pad=10, expand_x = True, enable_events = True)
        trip_length_input = sg.Input("", key="trip_length_in", font=("Times New Roman", 12), pad=10, expand_x = True, enable_events = True)
        destination_input = sg.Input("", key="destination_in", font=("Times New Roman", 12), pad=10, expand_x = True, enable_events = True)
        input_column = sg.Column([[trip_name_input], [start_date_input], [end_date_input], [trip_length_input], [destination_input]],
                                 expand_x = True)
        
        dummy_text1 = sg.Text("", pad=10)
        start_date_button = sg.CalendarButton("...", no_titlebar=False, close_when_date_chosen=True, format="%Y-%m-%d",
                                              target="start_date_in", auto_size_button=True, pad=10, tooltip="open calendar")
        end_date_button = sg.CalendarButton("...", no_titlebar=False, close_when_date_chosen=True,format="%Y-%m-%d",
                                            target="end_date_in", auto_size_button=True, pad=10, tooltip="open calendar")
        dummy_text2 = sg.Text("", pad=10)
        dummy_text3 = sg.Text("", pad=10)
        button_column = sg.Column([[dummy_text1],[start_date_button],[end_date_button],[dummy_text2],[dummy_text3]],
                                 expand_x = False)

        helper_text = sg.Text("Fields indicated with * must be filled", font=("Times New Roman", 10, "italic"))
        empty_line = sg.Text("")
        warning_message = sg.Text("", expand_x=True, justification="left", text_color="red", font=("Times New Roman", 10, "bold"))

        confirm_button = sg.Button("Confirm", tooltip="Create new trip", font=("Times New Roman", 12), key="confirm_new_trip", bind_return_key=True)
        cancel_button = sg.Button("Cancel", tooltip="Canel creation", font=("Times New Roman", 12), key="cancel_new_trip")
        clear_all_button = sg.Button("Clear all data", tooltip="Clear all input fields", font=("Times New Roman", 12), key="clear_fields")
        blanks = sg.Text(" "*115) #Used to formatting buttons
        clear_all_column = sg.Column([[clear_all_button, blanks]], element_justification="left", justification="left")
        confirm_cancel_column = sg.Column([[confirm_button, cancel_button]], element_justification="right", justification="right")

        new_trip_window = sg.Window("Splitwiser", [[title_text],
                                                   [text_column, input_column, button_column],
                                                   [helper_text],
                                                   [empty_line],
                                                   [warning_message],
                                                   [clear_all_column, confirm_cancel_column]],
                                                   size=(750,400), resizable=True, finalize=True)

        bindkey(new_trip_window, keybind_maps) # This should be moved to utility and import from there
        new_trip_window.bind('<Configure>', "resize_event")
        new_trip_window.set_min_size((750,400))

        #Set initial variables for detecting input errors
        start_date = "" #start_date and end_date will be date object
        end_date = ""
        trip_length = -1 #trip length is int
        warnings = set()

        while True:
            #Warning message update is set in front of while loop since some changes will do continue to go to next loop
            warning_message.update(value=("; ").join(list(warnings)))
            print(("; ").join(list(warnings)))

            event, values = new_trip_window.read()
            print(event)
            print(values)
            if event in (sg.WIN_CLOSED, "Exit::exitkey", "control-w", "exit_button", "cancel_new_trip"):
                new_trip_window.close()
                break
            
            elif event in ("clear_fields"):
                for field in [trip_name_input, start_date_input, end_date_input, trip_length_input, destination_input]:
                    field.update("", background_color="white")
            
            elif event in ("resize_event"):
                blanks.update(" "*(round((new_trip_window.Size[0]-290)/460*115))) #This is to always put clear all data on the lefe hand side
            
            elif event in ("start_date_in"):
                start_date_text.update(text_color="black")
                if values["start_date_in"] == "":
                    start_date = ""
                    start_date_input.update(background_color="white")
                    warnings.discard("Invalid start date")
                    warnings.discard("End date is earlier than start date")
                    continue
                try:
                    start_date = date.fromisoformat(values["start_date_in"])
                    print(start_date)
                except ValueError as e:
                    error_str = str(e)
                    start_date_input.update(background_color="indian red")
                    start_date = ""
                    warnings.add("Invalid start date")
                else:
                    warnings.discard("Invalid start date")
                    start_date_input.update(background_color="white")
                    if end_date != "":
                        if end_date < start_date:
                            end_date_input.update(background_color="indian red")
                            warnings.add("End date is earlier than start date")
                        else:
                            trip_length = (end_date - start_date).days
                            trip_length_input.update(value = trip_length, background_color="white")
                            end_date_input.update(background_color="white")
                            warnings.discard("End date is earlier than start date")
                    elif trip_length != -1:
                        end_date = str(start_date + timedelta(trip_length))
                        end_date_input.update(value = end_date, background_color="white")

            elif event in ("end_date_in"):
                end_date_text.update(text_color="black")
                trip_length_text.update(text_color="black")
                if values["end_date_in"] == "":
                    end_date = ""
                    end_date_input.update(background_color="white")
                    warnings.discard("Invalid end date")
                    warnings.discard("End date is earlier than start date")
                    continue
                try:
                    end_date = date.fromisoformat(values["end_date_in"])
                except ValueError as e:
                    end_date_input.update(background_color="indian red")
                    end_date = ""
                    warnings.add("Invalid end date")
                else:
                    warnings.discard("Invalid end date")
                    end_date_input.update(background_color="white")
                    if start_date != "":
                        if end_date < start_date:
                            end_date_input.update(background_color="indian red")
                            warnings.add("End date is earlier than start date")
                        else:
                            trip_length = (end_date - start_date).days
                            trip_length_input.update(value = trip_length, background_color="white")
                            end_date_input.update(background_color="white")
                            warnings.discard("End date is earlier than start date")

            elif event in ("trip_length_in"):
                end_date_text.update(text_color="black")
                trip_length_text.update(text_color="black")
                if values["trip_length_in"] == "":
                    trip_length = -1
                    trip_length_input.update(background_color="white")
                    warnings.discard("Invalid trip length")
                    continue
                try:
                    trip_length = int(values["trip_length_in"])
                    if trip_length < 0:
                        raise ValueError
                except ValueError as e:
                    trip_length_input.update(background_color="indian red")
                    trip_length = -1
                    warnings.add("Invalid trip length")
                else:
                    trip_length_input.update(background_color="white")
                    warnings.discard("Invalid trip length")
                    if start_date != "":
                        end_date = start_date + timedelta(trip_length)
                        end_date_input.update(value = str(end_date), background_color="white")
            
            elif event in ("trip_name_in"):
                trip_name_text.update(text_color="black")
                trip_name = values["trip_name_in"]
                if trip_name == "":
                    trip_name_input.update(background_color="white")
                    warnings.discard("Trip name must start with letter, and only allowed special characters are - and _")
                    continue
                has_invalid_char = False
                for char in trip_name:
                    if char not in ascii_letters+digits+"_"+"-"+" ":
                        has_invalid_char = True
                if has_invalid_char or (trip_name and trip_name[0]) not in ascii_letters:
                    trip_name_input.update(background_color="indian red")
                    warnings.add("Trip name must start with letter, and only allowed special characters are - and _")
                else:
                    trip_name_input.update(background_color="white")
                    warnings.discard("Trip name must start with letter, and only allowed special characters are - and _")

            elif event in ("confirm_new_trip"):
                missing_field = []
                if warnings:
                    sg.popup(("\n").join(list(warnings)), title="Error", button_justification="c", font=("Times New Roman", 12),
                             keep_on_top=True, custom_text="Cancel")
                    continue
                if values["trip_name_in"] == "":
                    missing_field.append("trip name")
                    trip_name_text.update(text_color="indian red")
                if values["start_date_in"] == "":
                    missing_field.append("start date")
                    start_date_text.update(text_color="indian red")                 
                if values["end_date_in"] == "" and values["trip_length_in"] == "":
                    missing_field.append("end date or trip length")
                    end_date_text.update(text_color="indian red")
                    trip_length_text.update(text_color="indian red")
                if missing_field:
                    sg.popup("Must enter the following fieds: %s." % (", ".join(missing_field)), title="Error", button_justification="c",
                             font=("Times New Roman", 12), keep_on_top=True, custom_text="Cancel")
                    continue
               
                print(missing_field)
                trip_name = values["trip_name_in"]
                start_date = date.fromisoformat(values["start_date_in"])
                end_date = date.fromisoformat(values["end_date_in"]) if values["end_date_in"] else ""
                trip_length = timedelta(int(values["trip_length_in"])) if values["trip_length_in"] else ""
                destination = values["destination_in"] if values["trip_length_in"] else None
                if end_date:
                    new_trip = Trip(trip_name, start_date, end_date = end_date, destination = destination)
                else:
                    new_trip = Trip(trip_name, start_date, length = trip_length, destination = destination)
                print(new_trip)
                self.new_trip = new_trip
                self.create_success = 1
                new_trip_window.close()
                break


if __name__ == "__main__":
    ntg = NewTripGui()
    ntg.preproc()
    ntg.create_new_trip(1)
    try:
        print(ntg.new_trip)
    except:
        print("No new trip")