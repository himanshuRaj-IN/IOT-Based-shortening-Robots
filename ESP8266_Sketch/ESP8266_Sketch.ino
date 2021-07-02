//commit 1
void setup()
{
  pinMode(13, OUTPUT);  //Assign the on board LED to pin 13
}

void loop() 
{
  blinkLED(3,500);
  delay(2000);
}

void blinkLED(int noTimes, int time)
{
  for (int i=1; i<= noTimes; i++)
  {
    digitalWrite(13, HIGH);
    delay(time);
    digitalWrite(13, LOW);
    delay(time);
  }
}
