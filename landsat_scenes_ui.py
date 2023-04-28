import tkinter as tk
from tkinter import *
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

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (450 // 2)
y = (screen_height // 2) - (100 // 2)

# Set the window's position to the center of the screen
window.geometry("+{}+{}".format(x, y))
window.title("IID - Landsat Scene Downloader")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                                                                        
def main_frame():

    window.geometry("450x100")
    window.minsize(450,100)    

    for widget in window.pack_slaves():
        widget.pack_forget()

    def start_search_button_clicked():
        global scene_list
        scene_list = landsat_scenes_downloader.StartSearch(window, start_date_entry, end_date_entry, download_button, landsat_value, list_display, single_download_button, start_search_button)
    
    def create_data_entry_widget(r, c):
        date_entry = DateEntry(main_frame, width = 12, justify = 'center', date_pattern = 'yyyy/mm/dd',background = 'white', foreground = 'red', borderwidth = 2, year = 2023)
        date_entry.grid(row = r, column = c, padx = 5, pady = 0)
        return date_entry
    
    def create_label(textString, r, c):
        label = tk.Label(main_frame, text = textString)
        label.grid(row = r, column = c, padx = 5, pady = 5)
        return label
    
    def create_button(textString, r, c, action):
        button = tk.Button(main_frame, text = textString, width = 11, command = action)
        button.grid(row = r, column = c, padx = 5, pady = 5)
        return button

    main_frame = Frame(window)
    main_frame.pack(padx = 1,pady = 1)

    # Create a label to display Start Date Input
    start_label = create_label("Start Date", 0, 0)

    # Create a DateEntry widget for user input (Start Date)
    start_date_entry = create_data_entry_widget(1, 0)

    # Create a label to display End Date Input
    end_label = create_label("End Date", 0, 1)

    # Create a DateEntry widget for user input (End Date)
    end_date_entry = create_data_entry_widget(1, 1)

    # Create a label to display Landsat Number input.
    landsat_number_label = create_label("Landsat Number", 0, 2)

    # Create a dropdown menu for landsat number:
    landsat_options = ['8', '9', '8/9']
    landsat_value = tk.StringVar()
    landsat_value.set(landsat_options[2])
    max_len = max([len(option) for option in landsat_options])

    drop_down_menu = tk.OptionMenu(main_frame, landsat_value, *landsat_options)
    drop_down_menu.config(width = max_len, anchor = 'center')
    drop_down_menu.grid(row = 1, column = 2, padx = 5, pady = 0)

    # Create a button to start landsat scene search.
    start_search_button = create_button("Start Search", 3, 1, start_search_button_clicked)

    # Create a button to download available scenes.
    download_button = create_button("Download All", 3, 1, lambda: landsat_scenes_downloader.start_download(download_button, scene_list))
    download_button.grid_remove()
    
    # Create a button to download single scenes.
    single_download_button = create_button("Single Download", 3, 2, single_download_frame)
    single_download_button.grid_remove()

    # Create a list to display the list of landsat scenes
    list_display = tk.Text(window, height = 50, width = 150)
    list_display.tag_configure('blue_tag', foreground = 'blue')
    list_display.tag_configure('green_tag', foreground = 'green')
    list_display.tag_configure('red_tag', foreground = 'red')
    list_display.tag_configure('center', justify = 'center')
    list_display.grid_forget()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def single_download_frame():

    window.geometry("450x150")
    window.minsize(450, 150)
    window.maxsize(450,150)

    for widget in window.pack_slaves():
        widget.pack_forget()
    
    single_download_frame = tk.Frame(window)
    single_download_frame.pack(padx = 1,pady = 1)

    landsat_data_entry_label = tk.Label(single_download_frame, text = 'Select Landsat Scene Below')
    landsat_data_entry_label.pack(padx = 1, pady = 1)

    landsat_options = scene_list
    landsat_scene = tk.StringVar()
    landsat_scene.set(landsat_options[0])

    scene_list_dropDown = tk.OptionMenu(single_download_frame, landsat_scene, *landsat_options)
    scene_list_dropDown.pack(padx = 1, pady = 5)

    download_button = tk.Button(single_download_frame, text = "Download Image", command = lambda: landsat_scenes_downloader.download_single_image(landsat_scene))
    download_button.pack(padx = 1, pady = 5)

    go_back = tk.Button(single_download_frame, text = "Back To Main Menu", command = main_frame)
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






        