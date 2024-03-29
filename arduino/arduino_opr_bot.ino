/*
Arduino Mega Controller for CGBOT-OPR

Arduino Mega Devices and Pins:

ULTRASONIC SENSORS:
* In a top down view. Robot front at the top.
    1               2               3
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
   8   @                        @    4
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
       @                        @
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    7              6              5

echo, trigger
1: 22,2
2: 23,3
3: 24,4
4: 25,5
5: 26,6
6: 27,7
7: 28,8
8: 29,9

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
int sensors[][2] = { {22, 2}, {23, 3}, {24, 4}, {25, 5}, {26, 6}, {27, 7}, {28, 8}, {29,9} };

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

    switch (menuChoice) {
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
                message += ", "
              }
            }
            message += "}";
            Serial.println(message);
        case 2:
            // Return Temperature on top/high/hot side
            float t = sht31.readTemperature();
            Serial.println(t);
        case 3:
            // Return humidity on low/cool side
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

