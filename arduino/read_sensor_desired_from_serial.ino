int temp;
int Rh;
int pressure;

void setup() {
  Serial.begin(9600);

  Serial.println("1. Temperature");
  Serial.println("2. Humidity");
  Serial.println("3. Barometric Pressure");
}

void loop() {

  while (Serial.available() == 0) {
  }

  int menuChoice = Serial.parseInt();

  switch (menuChoice) {
    case 1:
      // temp sensor code goes here
      Serial.print("The temperature is: ");
      Serial.println(temp);
      break;

    case 2:
      // humidity sensor code goes here
      Serial.print("The humidity is: ");
      Serial.println(Rh);
      break;

    case 3:
      // pressure sensor code goes here
      Serial.print("The barometric pressure is: ");
      Serial.println(pressure);
      break;

    default:
      Serial.println("Please choose a valid selection");
  }
}