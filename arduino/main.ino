#include <DHT.h>

const int PIN_DHT = 4;

DHT dht(PIN_DHT, DHT11);

void setup() {
  Serial.begin(9600);
  
  dht.begin();
}

void loop() { 
  float humidity    = dht.readHumidity();
  float temperature = dht.readTemperature();

  Serial.println("h" + humidity);
  Serial.println("t" + temperature);

  delay(500);
}
