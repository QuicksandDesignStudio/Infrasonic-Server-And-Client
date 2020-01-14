float timeKeeper;
float samplingTime = 500;

void setup() {
  timeKeeper = micros();
  Serial.begin(57600);

}

void loop() {
  float currentTime = micros();
  if((currentTime - timeKeeper) > samplingTime) {
    timeKeeper = micros();
    int value = int(analogRead(A4));
    Serial.println(value);
  }
}
