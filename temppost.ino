#include "max6675.h"


int thermoDO = 9;
int thermoCS = 8;
int thermoCLK = 13;

MAX6675  thermocouple(thermoCLK, thermoCS, thermoDO);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(thermocouple.readCelsius());
  delay(1000);

}
