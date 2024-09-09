# Indoor-Localization
The first phrase of the project tries to carry out war driving in Chi Wah Learning Commons to find out the position of routers using variuos methods on the provideed map.
The second phrase of the project tries to locate the router in a classroom. Among the four methods, trilateration and machine learning approach give the best accuracy. 

-------------------------------------------------------------------------------------------------------------

## For setup the ESP32 and the MQTT
please look at the folder ESP32_Setup and the mqttControlAndDataProcess.py.

## For testing localization algorithms using the dataset:
Approach 1: localization_max.py 

Approach 2: localization_weighted.py

Approach 3 & 4: localization_trilateration.py

Approach 5: ml folder

## For testing war-driving:

ardriving_data_processing.py
wardriving_trilateration.py


## For viewing results of the wardriving in chi wah commons:

war_driving_result.jpeg
