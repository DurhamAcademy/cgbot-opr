void setup() {
  Serial.begin(9600);
}
void loop() {
  Serial.println("Hello World");
  delay(1000);
}

/*
  RB-Dfr-720 :: Weatherproof Ultrasonic Sensor w/ Separate Probe
  http://www.robotshop.com/en/weatherproof-ultrasonic-sensor-separate-probe.html


//#define ECHOPIN 22 // Pin to receive echo pulse
//#define TRIGPIN 2 // Pin to send trigger pulse

// [ [echo, trigger] ]
int sensors[][2] = { {22, 2}, {23, 3} };

void setup(void)
{
  Serial.begin(9600);
  
  for (int i = 0; i < sizeof sensors/sizeof sensors[0]; i++) {
    pinMode(sensors[i][0], INPUT);
    pinMode(sensors[i][1], OUTPUT);
    digitalWrite(sensors[i][0], HIGH);
  }
}

void loop(void)
{
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

  // Wait 50mS before next ranging
  delay(50);
}
*/
