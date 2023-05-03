# <h1 align = "center"> **LANDSAT SCENE DOWNLOADER** </h1>

# <h2 align = "left"> **PROJECT DESCRIPTION** </h2>

Irrigation companies that provide water to farmers and ranchers for agricultural purposes rely heavily on satellite imagery to support their water consumption and water conservation data analysis. Company "X"  currently follows a set of procedures to search, acquire, format, process and analyze a single landat scene at a time. This whole process can take an engineer in Company "X" between 10 - 15 minutes, depending on the engineer's familiarization with the process.

While looking for solutions to make this process easier, more user-friendly and less time consuming, a python script that uses multiple packages including **PANDAS**, **EE**, **TKINTER** was developed to tackle these main issues.

# <h2 align = "left"> **CURRENT PROCEDURES IN PLACE** </h2>

- Log in to https://earthexplorer.usgs.gov 
- Define Path and Row as the Geocoding method. Path and Row are used to locate the area you are interested in. In this case, Company "X" is located in the Imperial Valley, California. Therefore, they would use the appropriate path and row to localate their location.
- Define a range of dates to search for landsat scenes.
- Download all the files provided. These files include metadata files and a series of multispectral images.
- Import images to GIS (Geographic Information Systems). 
- Process multispectral images using Band 3, Band 4 and Band 5. Band 5 measures radiation in the near-infrared region of the electromagnetic spectrum. This band is particularly useful for detecting vegetation, as healthy vegetation strongly reflects near-infrared radiation. 
- Create a single image from Band 3, Band 4 and Band 5.
- Image is now ready to be used for analysis purposes.

# <h2 align = "left"> **PROPOSED PROCEDURES** </h2>
- Run Script
![Alt Text](Screenshots/STEP_1.png)
- Select Start Date, End Date and Landsat Number (landsat 8 and 9 are two different satellites in orbit).
![Alt Text](Screenshots/STEP_2.png)
- Start Search and choose to "Download All" scenes found or "Single Download" a scene.
![Alt Text](Screenshots/STEP_3.png)
- If "Single" Download was selected, choose the desired scene from the list provided.
![Alt Text](Screenshots/STEP_4.png)
- Image will download directly to your current work directory and is ready to be used with GIS.
![Alt Text](Screenshots/SCENE.png)











 