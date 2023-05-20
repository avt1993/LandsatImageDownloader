# <h1 align = "center"> **LANDSAT SCENE DOWNLOADER SCRIPT** </h1>

# <h2 align = "left"> **PROJECT DESCRIPTION** </h2>
Irrigation companies that provide water to farmers and ranchers for agricultural purposes rely heavily on satellite imagery to support their water consumption and water conservation data analysis. Company "X"  currently follows a set of procedures to search, acquire, format, process and analyze a single landat scene at a time. This whole process can take an engineer in Company "X" between 10 - 15 minutes, depending on the engineer's familiarization with the process.

While looking for solutions to make this process easier, more user-friendly and less time consuming, a python script that uses multiple packages including **PANDAS**, **EE**, **TKINTER** was developed to tackle these main issues.

# <h2 align = "left"> **CURRENT PROCEDURES** </h2>
# <h3 align = "left"> **Listed below are the current steps to acquire a single landsat scene:** </h3>
- Log in to https://earthexplorer.usgs.gov 
- Define Path and Row as the Geocoding method. The path and row system is used to identify specific locations on the Earth's surface for satellite imagery acquisition and retrieval. In this case, Company "X" is located in Imperial Valley, California. Therefore, they would use the appropriate path and row to locate this area of interest.
- Define a range of dates to search for landsat scenes.
- Download all the files provided. These files include metadata files and a series of multispectral images.
- Import images to GIS (Geographic Information Systems). 
- Process multispectral images using Band 3, Band 4 and Band 5. Band 5 measures radiation in the near-infrared region of the electromagnetic spectrum. This band is particularly useful for detecting vegetation, as healthy vegetation strongly reflects near-infrared radiation. 
- Create a single image from Band 3, Band 4 and Band 5.
- Image is now ready to be used for analysis purposes.

# <h2 align = "left"> **PROPOSED PROCEDURES** </h2>
# <h3 align = "left"> **Listed below are the proposed steps to acquire landsat scenes:** </h3>

- Run Script
![Alt Text](Screenshots/STEP_1.png)
- Select Start Date, End Date and Landsat Number (landsat 8 and 9 are two different satellites in orbit).
![Alt Text](Screenshots/STEP_2.png)
- Start Search and choose to "Download All" scenes found or "Single Download" a scene.
![Alt Text](Screenshots/STEP_3.png)
- If "Single" Download was selected, choose the desired scene from the list provided.
![Alt Text](Screenshots/STEP_4.png)
- Image will download directly to your current work directory and is ready to be imported into GIS for further analysis.
![Alt Text](Screenshots/SCENE.png)

# <h2 align = "center"> **KEY DIFFERENCES BETWEEN CURRENT AND PROPOSED PROCEDURES** </h2>
- One key difference is that the proposed procedures will process and download all landsat scenes and ready to be used without additional time and resources spent by having to combine bands into one single image. Previously, the engineer in charge would need to import B3, B4 and B5 into GIS and manually combine the bands to create a single landsat scene. Since we know that Company "X" only uses B3, B4 and B5 during their analysis, we hard coded the script to only process and download images with these three bands. By doing so, the engineer will no longer need to do this by hand which is one of the longer steps to accomplish with the current procedures. The image will be downloaded ready to be imported into GIS as is.
- The engineer will no longer need to store and manage hundreds of different files and images at once. The current procedure generates about 20 files totalling about 1GB of size per scene downloaded. The proposed procedure will only generate one single image totalling about 20MB in size and will be ready to be stored and used for further analysis. Not only is the process simpler and more efficient, but will increase memory storage.
- Since Company "X" is only interested in analyzing landsat scenes from the Imperial Valley, we have also hard coded the path and row that correspond to this area of interest into the script and thus making the retrival of the scenes faster.

# <h1 align = "center"> **LANDSAT SCENE DOWNLOADER PYTHON SCRIPTS** </h1>

# <h2 align = "left"> **landsat_scenes_ui.py** </h2>
**landsat_scenes_ui.py** is the main script of this project. This script contains the code to generate the GUI. Tkinter was used to develop the Graphical User Interface of this project. Tkinter is the standard GUI (Graphical User Interface) package for Python, and it is included with most Python installations. It provides a set of tools and widgets for creating desktop GUI applications with Python. 

There are two main functions inside the main script. Each function controls one of two frames available for the user to interact with. One function contains code for the main frame called **main_frame()**. This is the frame the user will see and interact with when the program intitially runs. The second function called **single_download_frame()** will be called when the **Single Button** is clicked. This means the user only wants to download a single scene from the list of scenes found. 

- **main_frame()**
![Alt Text](Screenshots/STEP_1.png)
- **single_download_frame()**
![Alt Text](Screenshots/SINGLE_DOWNLOAD_FRAME.png)

# <h2 align = "left"> **landsat_scenes_downloader.py** </h2>

**landsat_scenes_ui.py** imports a module called **landsat_scene_downloader.py**. This module that works on the back end is the "server". Its function is to perform all the necessary tasks to search and download the landsat scenes requested by the user. 

**landsat_scene_downloader.py** contains multiple functions:
- **start_search()** function will read user input and check certain conditions are met before calling on other functions to perform the next steps.
![Alt Text](Screenshots/start_search().png)

- **ee_image_collection_toList()** function will use Google Earth Engine API to search for available landsat scenes that meet our criteria. A list of landsat scenes will be created.
![Alt Text](Screenshots/ee_image_collection_toList().png)

- **start_download()** function will use threads to download the complete list of available scenes. this function will call on **download_scene()**.
![Alt Text](Screenshots/start_download().png)

- **download_scene()** function will use **EE** and **GEEMAP** packages to select and download each single landsat scene. 
![Alt Text](Screenshots/download_scene().png)

- **download_single_image()** function will be called on when the user only wants to download one single landsat scene.
![Alt Text](Screenshots/download_single_image().png)













 