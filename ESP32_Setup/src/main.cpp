#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <iostream>
#include <fstream>
#include <SPIFFS.h>


const char* ssid = "Winnie";
const char* pass = "12345678";
const char* broker = "172.20.10.3"; //IP of hotspot
const char* outTopic = "SENSOR_DATA";
const char* inTopic = "COMMANDS";

WiFiClient espClient;
PubSubClient client(espClient);
long currentTime, lastTime;
int count = 0;
char msg[75];
bool shouldPublish = false;  // Global flag to control publishing


void setupWifi(){
    delay(100);
    Serial.println("\nConnecting to");
    Serial.println(ssid);

    WiFi.begin(ssid, pass);

    while(WiFi.status() != WL_CONNECTED){
        delay(1000);
        Serial.print("-"); //if the wifi is not connected, print a dot every 100ms
    }

    Serial.println("\nConnected to wifi");
    Serial.println(ssid); //if the Wifi is connected, print the ssid
}



void reconnect() {
    while(!client.connected()){
        Serial.print("\nConnecting to ");
        Serial.println(broker);
        if(client.connect("Winnie")){
            Serial.print("Connected to broker");
            Serial.println(broker);
            client.subscribe(inTopic); 
        }else{
            Serial.print("Trying to connect again");
            delay(5000);
        }
    }
}

void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Received message on topic: ");
    Serial.println(topic);
    Serial.print("Message: ");
    String message = "";
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    Serial.println(message);

    if (message == "start") {
        shouldPublish = true;
    } else if (message == "stop") {
        shouldPublish = false;

    }
}

void setup() {
  Serial.begin(9600);
//   if (!SPIFFS.begin(true)) {
//         Serial.println("An Error has occurred while mounting SPIFFS");
//         return;
//     }
  setupWifi();
  client.setServer(broker, 1883);
  client.setCallback(callback);
  client.subscribe("COMMANDS");

}


int counter = 0;

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    if (shouldPublish) {
        Serial.println("Scan start");
        counter++;
        // WiFi.scanNetworks will return the number of networks found.
        int n = WiFi.scanNetworks();
        Serial.println("Scan done");
        if (n == 0) {
            Serial.println("no networks found");
        } else {
            Serial.print(n);
            // open file 
            // File file = SPIFFS.open("/output.csv", FILE_APPEND);
            // // std::ofstream file;
            // // file.open("output", std::ios::app);
            // if (!file) {
            //     Serial.println("Failed to open file for appending");
            //     return;
            // }
            Serial.println(" networks found");
            Serial.println("Nr | SSID                             | RSSI | CH | Encryption");
            for (int i = 0; i < n; ++i) {
                // output to output.csv file
                // if (WiFi.SSID(i) == "HKU") {
                //     file.printf("%4d,%d\n", WiFi.RSSI(i), WiFi.encryptionType(i));
                //     // file << WiFi.RSSI(i) + "," + WiFi.encryptionType(i) << std::endl;
                // }

                // 1. restart mosquitto
                // 2. upload to esp32
                // 3. turn on hotspot 
                // 5. turn on serial : connect to broker 
                // 4. connect computer to hotspot 
                // 6. run python script 
                // 7. click start in UI menu


                // Print SSID and RSSI for each network found
                Serial.printf("%2d",i + 1);
                Serial.print(" | ");
                Serial.printf("%-32.32s", WiFi.SSID(i).c_str());
                Serial.print(" | ");
                Serial.printf("%4d", WiFi.RSSI(i));
                Serial.print(" | ");
                Serial.printf("%2d", WiFi.channel(i));
                Serial.print(" | ");
                switch (WiFi.encryptionType(i))
                {
                case WIFI_AUTH_OPEN:
                    Serial.print("open");
                    break;
                case WIFI_AUTH_WEP:
                    Serial.print("WEP");
                    break;
                case WIFI_AUTH_WPA_PSK:
                    Serial.print("WPA");
                    break;
                case WIFI_AUTH_WPA2_PSK:
                    Serial.print("WPA2");
                    break;
                case WIFI_AUTH_WPA_WPA2_PSK:
                    Serial.print("WPA+WPA2");
                    break;
                case WIFI_AUTH_WPA2_ENTERPRISE:
                    Serial.print("WPA2-EAP");
                    break;
                case WIFI_AUTH_WPA3_PSK:
                    Serial.print("WPA3");
                    break;
                case WIFI_AUTH_WPA2_WPA3_PSK:
                    Serial.print("WPA2+WPA3");
                    break;
                case WIFI_AUTH_WAPI_PSK:
                    Serial.print("WAPI");
                    break;
                default:
                    Serial.print("unknown");
                }
                Serial.print(" | ");

                const uint8_t* bssid = WiFi.BSSID(i);
                if (bssid != nullptr) {
                    Serial.printf("%02X:%02X:%02X:%02X:%02X:%02X", bssid[0], bssid[1], bssid[2], bssid[3], bssid[4], bssid[5]);

                    // String message = "SSID: " + String(WiFi.SSID(i)) + " RSSI: " + String(WiFi.RSSI(i)) + " CH: " + String(WiFi.channel(i)) + " Encryption: " + String(WiFi.encryptionType(i)) + " BSSID: " + String(bssid[0], HEX) + ":" + String(bssid[1], HEX) + ":" + String(bssid[2], HEX) + ":" + String(bssid[3], HEX) + ":" + String(bssid[4], HEX) + ":" + String(bssid[5], HEX);
                    // if (WiFi.SSID(i) == "HKU") {
                    String message = String(WiFi.SSID(i)) + " " +
                                        String(WiFi.RSSI(i)) + " " +
                                        String(bssid[0], HEX) + ":" + String(bssid[1], HEX) + ":" + String(bssid[2], HEX) + ":" + String(bssid[3], HEX) + ":" + String(bssid[4], HEX) + ":" + String(bssid[5], HEX);

                    client.publish(outTopic, message.c_str());
                    // }
                } else {
                    Serial.print("N/A");
                }
                Serial.println();
                delay(10);
            }
            // file.close();   
        }
        Serial.println("");
    
        // Delete the scan result to free memory for code below.
        WiFi.scanDelete();
    
        // Wait a bit before scanning again.
        delay(200); //adjust this parameter to change scan interval
    }
    std::string end = "Round" + std::to_string(counter) + "\n";
    client.publish(outTopic, end.c_str());
}

