float voltage;

void setup() {
  Serial.begin(9600);
  analogReference(AR_DEFAULT);
}

void loop() {
  // calibrate reading
  voltage = analogRead(A1) * 0.01627 ; 
  Serial.println(voltage);
}