# End-to-End Indoor-Localization system based on Wi-Fi RSSI
The first phrase of the project tries to carry out war driving in Chi Wah Learning Commons to find out the position of routers using variuos methods on the provideed map.
The second phrase of the project tries to locate the router in a classroom. 

## Workflow
1. RSSI Data Collection: Get RSSI data from an IoT device
2. Data Transportation: Send the RSSI data to an edge/cloud server for processing
3. Localization Algorithm: Estimate the clientʼs location based on the collected RSSI data
4. System Evaluation: Evaluate the system performance both on benchmark datasets and in real-world scenarios.

## Implementations
#### For ESP32 setup, please refer to the folder ESP32_Setup 

#### For MQTT setup, please refer to mqttControlAndDataProcess.py
  
#### For localization algorithms on four differnt approaches: 
  1. localization_max.py 
  2. localization_weighted.py
  3. localization_trilateration.py
  4. ml folder

#### For war-driving on two approaches:
  1. ardriving_data_processing.py
  2. wardriving_trilateration.py


## Result and Findings
Overall, the wardriving and indoor-localization system are successfully implemented and the performance are satisfactory. For more, the detailed report can be found in the Final_Report.pdf
