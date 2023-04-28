import tkinter as tk
from tkinter import *
from tkcalendar import DateEntry
import ee
import geemap
from termcolor import colored
import threading
import pandas as pd

scene_list = []

# Function that will export each scene based on the scene ID. 
def download_scene(scene_ID):
    IVregion = ee.Geometry.BBox(-115.90771, 33.4, -115.1, 32.6)
    image = ee.Image(scene_ID).select(['B5', 'B4', 'B3'])
    file_name = (scene_ID[24:44] + '.tif')
    geemap.ee_export_image(image, filename = file_name, scale = 45.4, region = IVregion)
    print(colored(scene_ID[24:44] + ' has successfully downloaded \n', 'green'))
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def start_download(download_button, scenelist):
    threads = []

    for scene in scenelist:
        thread = threading.Thread(target = download_scene, args = (scene,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(colored('\nALL SCENES HAVE SUCCESSFULLY DOWNLOADED.', 'white', 'on_green', attrs = ['bold']))
    download_button.grid_remove()
    scenelist = []
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def ee_image_collection_toList(LSN, start, end):
        LSN = '0' + LSN
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

    if (LSN == '8' or LSN == '9'):
        id_list = ee_image_collection_toList(LSN, start, end)

    else:
        id_list08 = ee_image_collection_toList('8', start, end)
        id_list09 = ee_image_collection_toList('9', start, end)
        id_list = id_list08 + id_list09

    return id_list
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function that prints out a list of scenes found for the date period and landsat number provided by the user.

def print_list(list, LSN):
        
    if (len(list) > 0):
        print('\nTHE FOLLOWING SCENES WERE FOUND: \n')

        for id in list:
            if ('LC08' in id):
                print(colored(id, 'green'))
                print('--------------------------------------------')
            else:
                print(colored(id, 'blue'))
                print('--------------------------------------------')
                    
        print('\n TOTAL LANDSAT ' + LSN + ' SCENES FOUND: ' + colored(str(len(list)), 'yellow', attrs= ['bold']))

    else:
        print(colored('\nNO IMAGES FOUND FOR THE SELECTED TIME PERIOD.', 'red', attrs = ['bold']))
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to clean date and leave only year - month - day. We are removing time since this is a datetime variable.
def date_conversion(date_input):

    year_value = str(date_input.year)
    month_value = str(date_input.month)
    day_value = str(date_input.day)

    date = year_value + '-' + month_value + '-' + day_value
            
    return date
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Function that will be called whenever the start search button is pressed. This function collects the input from the user and
    # calls on the date_conversion function, scene_finder function and print_list function. It also used a dataframe to order the list in
    # chronological order in case the user wants to print all landsat 8/9 scenes.

def StartSearch(window, start_date_entry, end_date_entry, download_button, landsat_value, list_display, single_download_button, start_search_button):

    global scene_list
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()

    if (start_date > end_date):
        print(colored("\nSTART DATE CANNOT BE AFTER END DATE. TRY AGAIN...", "red", attrs = ["bold"]))
        download_button.grid_remove()

    elif (start_date == end_date):
        print(colored("\nSTART DATE AND END DATE CANNOT BE THE SAME. TRY AGAIN...", "red", attrs = ["bold"]))
        download_button.grid_remove()

    else:    
        start_search_button.grid(row=3, column=0, padx=5, pady=5)
        landsat_number = landsat_value.get()

        start_date = date_conversion(start_date)
        end_date = date_conversion(end_date)

        if (landsat_number == '8' or landsat_number == '9'):

            scene_list = scene_finder(landsat_number, start_date, end_date)
            print_list(scene_list, landsat_number)

        else:
                    
            scene_list = scene_finder('8/9', start_date, end_date)

            # Used a dataframe to order landsat images chronologically.
            date_list = scene_list.copy()
            c = 0
            for i in date_list:
                date_list[c] = (date_list[c][36:44])
                c = c + 1
                    
            df = pd.DataFrame(list(zip(scene_list, date_list)), columns = ['Landsat Scene #', 'Date'])
            df = df.sort_values(by = ['Date']).reset_index(drop = True)
            scene_list = df['Landsat Scene #'].values.tolist()

            print_list(scene_list, landsat_number)

        if (len(scene_list) > 0):

            window.geometry("450x400")
            window.minsize(450, 150)
            window.maxsize(450,350) 

            list_display.pack()

            # Clear the Text widget
            list_display.config(state = 'normal')
            list_display.delete('1.0', tk.END)
            list_display.configure(font = ('Arial', 17))

            # Insert the list items into the Text widget
            for item in scene_list:
                if "LC08" in item:
                    list_display.insert(tk.END, item + "\n", "blue_tag")
                    list_display.insert(tk.END, "----------------------------------------------------------------------------\n")
                else:
                    list_display.insert(tk.END, item + "\n", "green_tag")
                    list_display.insert(tk.END, "----------------------------------------------------------------------------\n")

            list_display.insert(tk.END, 'TOTAL LANDSAT SCENES FOUND: ' + str(len(scene_list)), 'red_tag')

            # Disable the Text widget to prevent editing
            list_display.tag_add('center', '1.0', 'end')
            list_display.configure(state = 'disabled')

            download_button.grid(row=3, column=1, padx=5, pady=0)
            download_button.config(bg = "green")
            single_download_button.grid(row=3, column=2, padx=5, pady=5)
            single_download_button.config(bg = "green")

            return scene_list

