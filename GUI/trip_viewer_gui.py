import PySimpleGUI as sg
import sys, os
from pathlib import Path
from datetime import date, timedelta

sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent))
keybind_maps = {
    "<Control_R><w>":"control-w", "<Control_L><w>":"control-w", "<Control_R><W>":"control-w", "<Control_L><W>":"control-w",
    "<Control_R><n>":"control-n", "<Control_L><n>":"control-n", "<Control_R><N>":"control-n", "<Control_L><N>":"control-n"
}
THEME = "DefaultNoMoreNagging"
sg.theme(THEME)
from Trip import Trip

def bindkey(window, map): #TODO: This method appeaers multiple places in splitwiser, should be put into utility and import
    if not isinstance(window, sg.Window):
        raise TypeError("Input window is not a GUI window object")
    for k, v in map.items():
        window.bind(k, v)

class TripViewer(object):

    def __init__(self, trip):
        if not isinstance(trip, Trip):
            raise TypeError("Not a valid trip input")
        self.trip = trip

    def view(self):
        #all objects below are for left column
        title_text = sg.Text("Trip: " + self.trip.trip_name, font = ("Times New Roman", 16, "bold"), justification = "center", expand_x = True)
        start_date_text = sg.Text("Start date", font = ("Times New Roman", 12), pad = 10)
        end_date_text = sg.Text("End date", font = ("Times New Roman", 12), pad = 10)
        trip_length_text = sg.Text("Trip length (days)", font = ("Times New Roman", 12), pad = 10)
        destination_text = sg.Text("Destination", font = ("Times New Roman", 12), pad = 10)
        dummy_line1 = sg.Text("", pad = 10)
        people_text = sg.Text("People", font = ("Times New Roman", 12), pad = 10)
        trip_master_text = sg.Text("Trip master: ", font = ("Times New Roman", 12), pad = 10)
        
        start_date_input = sg.Input(key="start_date_in", font=("Times New Roman", 12), pad=10,
                                    expand_x = True, enable_events = True, default_text = str(self.trip.start_date))
        end_date_input = sg.Input(key="end_date_in", font=("Times New Roman", 12), pad=10,
                                  expand_x = True, enable_events = True, default_text = str(self.trip.end_date))
        trip_length_input = sg.Input(key="trip_length_in", font=("Times New Roman", 12), pad=10,
                                     expand_x = True, enable_events = True, default_text = self.trip.length.days)
        destination_input = sg.Input(key="destination_in", font=("Times New Roman", 12), pad=10,
                                     expand_x = True, enable_events = True, default_text = self.trip.destination)
        
        people_load = sg.Button("Load from another trip", key = "people_load_button", font = ("Times New Roman", 12), pad = 10)
        people_box = sg.Listbox(list(self.trip.people.keys()), key = "people_listbox", enable_events = True, font = ("Times New Roman", 12),
                                pad = 10, size = (45, 10))
        people_remove = sg.Button("Remove", key = "people_remove_button", font = ("Times New Roman", 12), pad = 10)
        people_edit = sg.Button("Edit", key = "people_edit_button", font = ("Times New Roman", 12), pad =10)
        people_add = sg.Button("Add", key = "people_add_button", font = ("Times New Roman", 12), pad = 10)

        trip_master_name = sg.Text(self.trip.trip_master, font = ("Times New Roman", 12))
        trip_master_change = sg.Button("Change", key = "change_tm", font = ("Times New Roman", 12))

        text_column = sg.Column([[start_date_text],
                                 [end_date_text],
                                 [trip_length_text],
                                 [destination_text]])
        
        input_column = sg.Column([[start_date_input],
                                  [end_date_input],
                                  [trip_length_input],
                                  [destination_input]], expand_x = True)
        
        tm_text_column = sg.Column([[trip_master_text, trip_master_name]], size = (300,100))
        tm_button_column = sg.Column([[trip_master_change]], element_justification = "right", size = (300,100))

        #all objects below are for right column
        expense_table_text = sg.Text("Expenses", font = ("Times New Roman", 12), pad = 10)
        table_header = ["ID", "Date", "Price", "location", "Payer", "Spliters"]
        table_width = [5, 10, 8, 10, 8, 30]
        expense_table = sg.Table([], col_widths = table_width, auto_size_columns = False, font = ("Times New Roman", 12),
                                 header_font = ("Times New Roman", 12, "bold"), expand_x = True, justification = "center",
                                 headings = table_header, enable_events = True, key = "expense_table", pad = 10)
        expense_remove = sg.Button("Remove", key = "expense_remove", font = ("Times New Roman", 12), pad = 10)
        expense_edit = sg.Button("Edit", key = "expense_edit_button", font = ("Times New Roman", 12), pad = 10)
        expense_add = sg.Button("Add", key = "expense_add_button", font = ("Times New Roman", 12), pad = 10)

        dummy_line2 = sg.Text("")
        split_table_text = sg.Text("Split table", font = ("Times New Roman", 12), pad = 10)
        split_table = sg.Multiline("", disabled = True, font = ("Times New Roman", 12), expand_x = True, size = (20, 8), pad = 10)

        #close and save buttons
        close_button = sg.Button("Close", key = "close_button", font = ("Times New Roman", 12))
        save_button = sg.Button("Save", key = "save_button", font = ("Times New Roman", 12))

        left_column = sg.Column([[text_column, input_column],
                                 [dummy_line1],
                                 [people_text, people_load],
                                 [people_box],
                                 [people_remove, people_edit, people_add],
                                 [tm_text_column, tm_button_column]], size = (400,600))
        
        right_column = sg.Column([[expense_table_text],
                                  [expense_table],
                                  [expense_edit, expense_add, expense_remove],
                                  [dummy_line2],
                                  [split_table_text],
                                  [split_table]],
                                  expand_x = True, vertical_alignment = "top")
        
        save_and_close_column = sg.Column([[close_button, save_button]], expand_x = True, element_justification="right")

        viewer_window = sg.Window("Splitwiser", [[title_text],
                                                 [left_column, sg.VerticalSeparator(), right_column],
                                                 [save_and_close_column]],
                                                 resizable = True, finalize = True, size = (1300, 700))
        viewer_window.set_min_size((1300, 700))
        
        bindkey(viewer_window, keybind_maps) # This should be moved to utility and import from there
        viewer_window.bind('<Configure>', "resize_event")

        while True: #event loop
            event, values = viewer_window.read()
            print(event)
            print(values)
            if event in (sg.WIN_CLOSED, "control-w", "close_button"):
                viewer_window.close()
                break

if __name__ == "__main__":
    from Person import Person
    nm_trip = Trip("New Mexico trip", "2023-11-22", end_date = "2023-11-27")
    nm_trip.add_destination("New Mexico")
    bq = nm_trip.add_person("Liu", "Bingqian", sex = "female")
    hy = nm_trip.add_person("Ma", "Haoyue", sex = "female")
    jc = nm_trip.add_person("Jing", "Yingze", sex = "male")
    xy = nm_trip.add_person("Zhao", "Xianyuan", sex = "male")
    xd = nm_trip.add_person("Erdong", "Lu", sex = "male", age = 28, id='wyrda')
    nm_trip.set_trip_master("wyrda")

    abq_hotel = nm_trip.add_expense(413.40, "2023-11-22")
    abq_hotel.set_location("Albuquerque, NM")
    abq_hotel.add_spliters(["Liu_Bingqian_1","Ma_Haoyue_1","Jing_Yingze_1","Zhao_Xianyuan_1"])

    print("Printing abq hotel split")
    abq_hotel.show_split()
    abq_hotel.set_split_mode("by_value")
    abq_hotel.set_split_table({"wyrda":102.68})
    abq_hotel.set_individual_split("Zhao_Xianyuan_1",62.68)
    abq_hotel.show_split()
    abq_hotel.set_split_mode("by_percent")
    abq_hotel.set_individual_split("wyrda",0.3)
    abq_hotel.set_individual_split("Ma_Haoyue_1",0.1)
    abq_hotel.show_split()

    print(str(nm_trip.start_date))

    my_tv = TripViewer(nm_trip)
    my_tv.view()






