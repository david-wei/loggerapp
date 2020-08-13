LOGGERAPP README

1. Short introduction

    - This program is supposed to log temperature data as well as beam-profiler  fitdata into an influxdb database using Python 3. The GUI was made with dash. All plots were made using plotly.
    - Note that the GUI is only supposed to control the logging process. A seperate program was written for data analysis and plotting. This was done because I wanted to strictly seperate the database (possibly running on a server) from the logger app.
    - Connecting to the camera sensors was achieved by using the class 'cameras' from the beamprofiler program. Acquiring fit data by the cameras also built upon the preexisting class 'analyser', which was modified for this use case
    - Connecting to the temperature sensors was achieved by modifying the preexisting temperature logging program. A good guideline for the usage of the temperature sensor can be found here: https://www.picotech.com/download/manuals/usb-tc08-thermocouple-data-logger-programmers-guide.pdf.
    
    

2. Database and usage

    - The Data storage works with InfluxDB. For more info on how to query and analyse data stored in Influx, see https://docs.influxdata.com/influxdb/v1.7/.
    - Data is saved into a database right now running on localhost:8086 (see db_interface.initiatedb() for more info) called "DB". All logging measurements are written into the measurement "log". Each datapoint has two tags 'type' and 'sensor'.
    - For camera sensors the type is set to 'camera', and the sensor is a string following the logic "vendor + ' ' + camid+ ' '+ instance". So for example an entry in the database could have the tags {'type':'camera', 'sensor':'vrm 123 incoming'}. Beam data is written using the float fields 'vcenter', 'hcenter', 'largewaist', 'smallwaist' and 'angle'.
    - Note that one camera can have multiple measuring instances which all export fit data seperately. Each instance has their own ROI, which automatically "follows" the beams. It can also be manually moved in the GUI.
    - For temperature sensors the type is set to 'temperature', and the sensor is a name assigned to a handle via the config file. So the tag dictionary might look like {'type':'temperature','sensor':'temperaturesensor123'}. Temperature data is written using the float fields 'channel1', 'channel2' and so on.


3. GUI options

    - The program allows the user to turn the datalogging process on and off, and set the rate at which data is exported to the database.
    - It also lets the user see the latest beam images and fit data from all connected cameras.

    


4. Setup
    1. Install required modules and influx
        - Install InfluxDB from https://www.influxdata.com/
        - Install all drivers in the loggerapp/datalogger/driver folder
        - Open a command prompt and change the directory to where the program was copied
        - Run "pip install -r requirements.txt"
    2. Initiate Sensors
        - Include all sensors including their initial parameters in the "sensorconfig.xml" file.
        - For camera sensors, include the parameters 'vendor', 'camid' (both used to find and connect to the camera) and 'beam' (used to distinguish between multiple beams on one camera) as well as the desired initial 'roiparams' in the format '(x-Position,y-Position,width,height)' (in pixels). The Roiparams do not need to be very exact, as the program will automatically reset the ROI anyways.
        - For temperature sensors, include the parameter 'handle' used by the DLL to connect to each temperature sensor as well as 'tempid', a name that will be used for this specific device in the database.
        

    
    
    
5. Running the program
    - Run 'influxd.exe' from the InfluxDB install
    - Once again, open a command prompt and change the directory to the program directory
    - Run 'python run.py' 
    - You should see an output of the type "Running on https://IP:Port"
    - Open a browser window and copy-paste the adress
 