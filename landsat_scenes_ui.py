import tkinter as tk
from tkinter import * 
from tkinter import ttk
from tkcalendar import DateEntry
import ee
from termcolor import colored
import landsat_scenes_downloader


try:
    ee.Initialize()

except ee.EEException:
    ee.Authenticate()
    ee.Initialize()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create a new window
window = tk.Tk()
window.title("IID - Landsat Scene Downloader")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (450 // 2)
y = (screen_height // 2) - (100 // 2)

# Set the window's position to the center of the screen
window.geometry("+{}+{}".format(x, y))

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                                                                        
def main_frame():

    landsat_scenes_downloader.window_display_config(125, window) 
   
    for widget in window.pack_slaves():
        widget.pack_forget()

    def start_search_button_clicked():
        global scene_list
        scene_list = landsat_scenes_downloader.StartSearch(label, frame, canvas, scrollbar, window, message_label, start_date_entry, end_date_entry, download_button, landsat_value, single_download_button)
    
    def create_data_entry_widget(frame):
        date_entry = DateEntry(master = frame, width = 12, justify = 'center', date_pattern = 'yyyy/mm/dd',background = 'white', foreground = 'red', borderwidth = 2, year = 2023)
        date_entry.pack(pady = 5)
        return date_entry
    
    def create_label(textString, frame):
        label = ttk.Label(master = frame, text = textString)
        label.pack(pady = 5)
        return label
    
    def create_button(textString, r, c,  action, frame):
        button = ttk.Button(master = frame, text = textString, command = action)
        button.grid(row = r, column = c, padx = 5)
        return button

    top_frame = ttk.Frame(master = window)
    left_frame = ttk.Frame(master = top_frame)
    center_frame = ttk.Frame(master = top_frame)
    right_frame = ttk.Frame(master = top_frame)
    button_frame = ttk.Frame(master = window)

    # Create a label to display Start Date Input
    start_label = create_label("Start Date", left_frame)
    # Create a DateEntry widget for user input (Start Date)
    start_date_entry = create_data_entry_widget(left_frame)
    left_frame.pack(side = 'left', padx = 10)
    

    # Create a label to display End Date Input
    end_label = create_label("End Date", center_frame)
    # Create a DateEntry widget for user input (End Date)
    end_date_entry = create_data_entry_widget(center_frame)
    # Create a button to start landsat scene search.
    center_frame.pack(side = 'left', padx = 10)


    # Create a label to display Landsat Number input.
    landsat_number_label = create_label("Landsat Number", right_frame)
    # Create a dropdown menu for landsat number:
    landsat_options = ['08', '09', '08/09']
    landsat_value = tk.StringVar()
    landsat_value.set(landsat_options[2])
    drop_down_menu = tk.OptionMenu(right_frame, landsat_value, *landsat_options)
    #drop_down_menu.config(anchor = 'center')
    drop_down_menu.pack(pady = 5)
    right_frame.pack(side = 'left', padx = 10)

    top_frame.pack()

    start_search_button = create_button("Start Search", 0, 0, start_search_button_clicked, button_frame)
    # Create a button to download available scenes.
    download_button = create_button("Download All", 0, 1, lambda: landsat_scenes_downloader.start_download(download_button, scene_list), button_frame)
    download_button.config(state = "disabled")
    # Create a button to download single scenes.
    single_download_button = create_button("Single Download", 0, 2, single_download_frame, button_frame)
    single_download_button.config(state = "disabled")
    button_frame.pack(pady = 5)

    message_label = create_label("", window)
    message_label.pack_forget()

    # Create a Frame widget and a Canvas widget
    frame = tk.Frame(window)
    canvas = tk.Canvas(frame, width = 400, height = 125, scrollregion = (0,0,200,200))

    # Create a Label widget and add it to the Canvas widget
    label = tk.Label(canvas, text = "", justify = "center")
    canvas.create_window((0,0), window = label, anchor = "nw")

    # Create a Scrollbar widget and configure it to scroll the Canvas widget
    scrollbar = tk.Scrollbar(frame, orient = "vertical", command = canvas.yview)
    canvas.config(yscrollcommand = scrollbar.set)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def single_download_frame():

    landsat_scenes_downloader.window_display_config(150, window)

    for widget in window.pack_slaves():
        widget.pack_forget()
    
    single_download_frame = ttk.Frame(window)
    single_download_frame.pack(padx = 1,pady = 1)

    landsat_data_entry_label = ttk.Label(master = single_download_frame, text = 'Select Landsat Scene Below')
    landsat_data_entry_label.pack(padx = 1, pady = 1)

    landsat_options = scene_list
    landsat_scene = tk.StringVar()
    landsat_scene.set(landsat_options[0])

    scene_list_dropDown = tk.OptionMenu(single_download_frame, landsat_scene, *landsat_options)
    scene_list_dropDown.pack(padx = 1, pady = 5)

    download_button = ttk.Button(master = single_download_frame, text = "Download Image", command = lambda: landsat_scenes_downloader.download_single_image(landsat_scene))
    download_button.pack(padx = 1, pady = 5)

    go_back = ttk.Button(master = single_download_frame, text = "Back To Main Menu", command = main_frame)
    go_back.pack(padx = 1, pady = 5)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Start the main loop to display the window
print('|\n''|\n''|\n''|\n''|\n''|\n''|\n''|\n''|\n''|\n''|\n')
print(colored('                   LANDSAT 8/9 IMAGE DOWNLOADER                   ', 'white', 'on_yellow', attrs = ['bold']))
print(colored('                                                                  ', 'white', 'on_yellow'))
print(colored('                 Developed by: Antonio Villardaga                 ', 'white', 'on_yellow', attrs = ['bold']))
print('\n')

main_frame()

window.mainloop()






        