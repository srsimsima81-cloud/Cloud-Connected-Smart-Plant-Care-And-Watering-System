#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* API_URL = "https://YOUR-BACKEND.example.com/api/sensors/data";
const char* SIMULATOR_KEY = "REPLACE_WITH_DEVICE_INGESTION_KEY";
const char* DEVICE_ID = "PLANT-ESP32-001";
const int RELAY_PIN = 26;

// Safe educational wiring assumptions: use low-voltage sensors and a properly rated relay/driver.
// Never connect a mains pump directly to an ESP32 GPIO. Use an isolated relay/driver and appropriate power supply.

void setup(){ pinMode(RELAY_PIN,OUTPUT); digitalWrite(RELAY_PIN,LOW); Serial.begin(115200); WiFi.begin(WIFI_SSID,WIFI_PASSWORD); while(WiFi.status()!=WL_CONNECTED){delay(500);Serial.print('.');} Serial.println(" connected"); }
void loop(){
  if(WiFi.status()==WL_CONNECTED){
    float moisture=35.0; // Replace with calibrated ADC conversion from your soil sensor.
    float temperature=28.0; // Replace with DHT11/DHT22 reading.
    float humidity=60.0;
    float light=70.0;
    float tank=80.0;
    String body="{\"device_id\":\""+String(DEVICE_ID)+"\",\"soil_moisture\":"+String(moisture,1)+",\"temperature\":"+String(temperature,1)+",\"humidity\":"+String(humidity,1)+",\"light_level\":"+String(light,1)+",\"water_tank_level\":"+String(tank,1)+"}";
    HTTPClient http; http.begin(API_URL); http.addHeader("Content-Type","application/json"); http.addHeader("X-Simulator-Key",SIMULATOR_KEY); int code=http.POST(body); Serial.printf("API status: %d\n",code); http.end();
    HTTPClient control; control.begin(String(API_URL).substring(0,String(API_URL).indexOf("/api/sensors/data"))+"/api/devices/"+String(DEVICE_ID)+"/control-state"); control.addHeader("X-Simulator-Key",SIMULATOR_KEY); int c=control.GET(); if(c==200){String response=control.getString(); bool on=response.indexOf("\"pump_on\":true")>=0; digitalWrite(RELAY_PIN,on?HIGH:LOW); Serial.printf("Pump command: %s\n",on?"ON":"OFF");} control.end();
  }
  delay(10000);
}
