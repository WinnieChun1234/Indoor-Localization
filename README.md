# Indoor-Localization
The first phrase of the project tries to carry out war driving in Chi Wah Learning Commons to find out the position of routers using variuos methods on the provideed map.
The second phrase of the project tries to locate the router in a classroom. Among the four methods, trilateration and machine learning approach give the best accuracy. 

-------------------------------------------------------------------------------------------------------------

### For setup the ESP32 and the MQTT
please consult the folder ESP32_Setup and the mqttControlAndDataProcess.py.

### For testing localization algorithms using the dataset, please consult:
    1. Approach 1: localization_max.py 
    2. Approach 2: localization_weighted.py
    3. Approach 3 & 4: localization_trilateration.py
    4. Approach 5: ml folder

### For testing war-driving, please consult:
    1. wardriving_data_processing.py
    2. wardriving_trilateration.py

### For viewing results of the wardriving in chi wah commons, please consult:
    1. war_driving_result.jpeg
