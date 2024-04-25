/*
Arduino Mega Controller for CGBOT-OPR

Arduino Mega Devices and Pins:

ULTRASONIC SENSORS:
* In a top down view. Robot front at the top.
    1                              2
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    4                            3

trigger, echo
1: 48,46
2: 44,42
3: 34,36
4: 40,38

// Temperature Sensor
i2C

// Voltage Sensor
A0

*/

#include <Arduino.h>
#include <Wire.h>
#include "Adafruit_SHT31.h"

// Ultrasonics
// [ [echo, trigger] ]
int sensors[][2] = { {48, 46}, {44, 42}, {34, 36}, {40, 38} };

// Temperature SHT30-D
Adafruit_SHT31 sht31 = Adafruit_SHT31();
bool enableHeater = false;

// Voltage Sensors
float voltage;

void setup(void)
{
  Serial.begin(9600);

  // Ultrasonic Sensors Pinmode
  for (int i = 0; i < sizeof sensors/sizeof sensors[0]; i++) {
    pinMode(sensors[i][0], INPUT);
    pinMode(sensors[i][1], OUTPUT);
    digitalWrite(sensors[i][0], HIGH);
  }

  // wait for serial to connect - is this needed?
  //while (Serial.available() == 0) {
  //}

  // Voltage Sensor
  analogReference(DEFAULT);

}

void loop(void)
{
    int serialSelect = Serial.parseInt();

    switch (serialSelect) {
        case 1:
            // Print Ultrasonic results when receiving a 1 on the serial port
            String message = "{";
            for (int i = 0; i < sizeof sensors/sizeof sensors[0]; i++) {
              int echo = sensors[i][0];
              int trig = sensors[i][1];
              digitalWrite(trig, LOW);
              delayMicroseconds(2);

              // Send a 10uS high to trigger ranging
              digitalWrite(trig, HIGH);
              delayMicroseconds(10);

              // Send pin low again
              digitalWrite(trig, LOW);

              // Read in times pulse
              int distance = pulseIn(echo, HIGH,26000);
              distance= distance/58;

              if (distance < 50 && distance > 0) {
                message += String(i) + ': 1';
              } else {
                message += String(i) + ": 0";
              }
              if (i < sizeof sensors/sizeof sensors[0] - 1) {
                message += ", ";
              }
            }
            message += "}";
            Serial.println(message);
        case 2:
            // Return Temperature on top/high/hot side
            float t = sht31.readTemperature();
            Serial.println(t);
        case 3:
            // Return humidity on top/high/hot side
            float h = sht31.readHumidity();
            Serial.println(h);
        case 4:
            // Return voltage reading from battery
            voltage = analogRead(A1) * 0.01627 ;
            Serial.println(voltage);
        default:
            Serial.println("invalid");
    }

}

