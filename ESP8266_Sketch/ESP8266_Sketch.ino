
#include <ESP8266WiFi.h>

const char* ssid     = "iot";
const char* password = "project1234";


void setup() {
  Serial.begin(115200);
  delay(100);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  // ------------------------------------------
  }

  Serial.println("");
  Serial.println("WiFi connected");
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {

  Serial.println("Hello i Am Conected to internet");
  delay(2000);
}