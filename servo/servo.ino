
#include <Servo.h>
Servo myservo;
void setup() {
   
    Serial.begin(115200);
    myservo.attach(9);
    myservo.write(93);
}

void loop() {
  if(Serial.available() > 0){
    String command = Serial.readString();
    Serial.println("Received command: " + command);  // Debug print
    if(command.equals("stop")){
      myservo.write(93);
     
    }
    if(command.equals("left")){
      myservo.write(90); 
      
    }
    if(command.equals("right")){
      myservo.write(95); 
      
    }
    if(command.equals("continue")){
      myservo.write(93);
    }
  }
}
