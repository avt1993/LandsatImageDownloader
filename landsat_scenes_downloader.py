import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry
import ee
import geemap
from termcolor import colored
import threading
import pandas as pd

scene_list = []

# Function that will export each scene based on the scene ID. 
def download_scene(scene):
    IVregion = ee.Geometry.BBox(-115.90771, 33.4, -115.1, 32.6)
    image = ee.Image(scene).select(['B5', 'B4', 'B3'])
    file_name = (scene[24:44] + '.tif')
    geemap.ee_export_image(image, filename = file_name, scale = 45.4, region = IVregion)
    print(colored(scene[24:44] + ' has successfully downloaded \n', 'green'))
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def download_single_image(landsat_scene):
    landsat_number = landsat_scene.get()
    download_scene(landsat_number)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def start_download(download_button, scenelist):

    threads = []

    for scene in scenelist:
        thread = threading.Thread(target = download_scene, args = (scene, ))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(colored('\nALL SCENES HAVE SUCCESSFULLY DOWNLOADED.', 'white', 'on_green', attrs = ['bold']))
    download_button.grid_remove()
    scenelist = []
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def ee_image_collection_toList(LSN, start, end):
        
        id_list = []
        imageCollection = ee.ImageCollection('LANDSAT/LC' + LSN + '/C02/T1_TOA').filter(ee.Filter.eq('WRS_PATH', 39)).filter(ee.Filter.eq('WRS_ROW', 37)).filterDate(start, end)
        
        if (imageCollection.size().getInfo() > 0):
            for image in imageCollection.toList(imageCollection.size()).getInfo():
                image_id = image['id']
                id_list.append(image_id)
        
            return id_list
        else:
            return id_list
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function that will search for landsat scenes based on the information provided by the user.
def scene_finder(LSN, start, end):

    if (LSN == '08' or LSN == '09'):
        id_list = ee_image_collection_toList(LSN, start, end)

    else:
        id_list08 = ee_image_collection_toList('08', start, end)
        id_list09 = ee_image_collection_toList('09', start, end)
        id_list = id_list08 + id_list09

    return id_list

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Function to clean date and leave only year - month - day. We are removing time since this is a datetime variable.
def date_conversion(date_input):

    year_value = str(date_input.year)
    month_value = str(date_input.month)
    day_value = str(date_input.day)

    date = year_value + '-' + month_value + '-' + day_value
            
    return date
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def window_display_config (h, window):
    window.geometry("450x" + str(h))
    window.minsize(450, h)
    window.maxsize(450,h) 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
    # Function that will be called whenever the start search button is pressed. This function collects the input from the user and
    # calls on the date_conversion function, scene_finder function and print_list function. It also used a dataframe to order the list in
    # chronological order in case the user wants to print all landsat 8/9 scenes.

def StartSearch(label, frame, canvas, scrollbar, window, message_label, start_date_entry, end_date_entry, download_button, landsat_value, single_download_button):

    global scene_list
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()

    if (start_date > end_date):
        window_display_config(150, window)
        scrollbar.pack_forget()
        canvas.pack_forget()
        frame.pack_forget()
        message_label.config(text = "START DATE CANNOT BE AFTER END DATE. TRY AGAIN...", foreground = "red", font = 'Arial 12 bold')
        message_label.pack(pady = 10)


    elif (start_date == end_date):
        window_display_config(150, window)
        scrollbar.pack_forget()
        canvas.pack_forget()
        frame.pack_forget()
        message_label.config(text = "START DATE & END DATE CANNOT BE THE SAME. TRY AGAIN...", foreground = "red", font = 'Arial 12 bold')
        message_label.pack(pady = 10)

    else:   
        landsat_number = landsat_value.get()

        start_date = date_conversion(start_date)
        end_date = date_conversion(end_date)

        if (landsat_number == '08' or landsat_number == '09'):

            scene_list = scene_finder(landsat_number, start_date, end_date)

        else:
                    
            scene_list = scene_finder('08/09', start_date, end_date)

            # Used a dataframe to order landsat images chronologically.
            date_list = scene_list.copy()
            c = 0
            for i in date_list:
                date_list[c] = (date_list[c][36:44])
                c = c + 1
                    
            df = pd.DataFrame(list(zip(scene_list, date_list)), columns = ['Landsat Scene #', 'Date'])
            df = df.sort_values(by = ['Date']).reset_index(drop = True)
            scene_list = df['Landsat Scene #'].values.tolist()

        if (len(scene_list) > 0):
            if (len(scene_list) < 5):
                window_display_config(225, window)

            else:
                window_display_config(300, window)

            download_button.config(state = "normal") 
            single_download_button.config(state = "normal")

            message_label.config(text = 'TOTAL LANDSAT SCENES FOUND: ' + str(len(scene_list)), foreground = "green", font = 'Arial 18 bold')
            message_label.pack(pady = 5)

            label.config(text = '')
            my_str = "\n".join(scene_list)
            label.config(text = label.cget("text") + "\n" + my_str, font = 'Arial 15 bold')
            canvas.config(scrollregion = canvas.bbox("all"), height = canvas.winfo_reqheight())
            scrollbar.pack(side = "right", fill = "y")
            canvas.pack(side = "left", fill = "both", expand = True)
            frame.pack()

            download_button.grid(row = 0, column = 1, padx = 5, pady = 5)
            single_download_button.grid(row = 0, column = 2, padx = 5, pady = 5)

            return scene_list
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        


