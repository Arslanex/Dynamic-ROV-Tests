#include <Servo.h>
Servo ser;
int pos = 90, defPos = 90;
// Bilgisayardan gelen veri değişkeni
String incomingByte ;   

void setup() {
  Serial.begin(9600); // 9600 bandını aç
  ser.attach(9);      // servo pinini tanımla
  ser.write(pos);  
 
// servoyu başlangıç açısından başla - 90
}
void loop() {
  if (Serial.available() > 0) // eğer haberleşme var ise
  {
    incomingByte = Serial.readStringUntil('\n'); // gelen değeri oku ve eşitle
    Serial.write("Com is Avaliable");
    if (incomingByte == "L")                     // gelen değer L(left) ise 
    {
        pos = pos -10;
    }
    else if (incomingByte == "R")                // gelen değer R(right) ise 
    {
        pos = pos +10;
    }
    else{
        pos = defPos;
    }
    ser.write(pos);  
  }
} 
