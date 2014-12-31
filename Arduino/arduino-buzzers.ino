/*
Trivia buzzer connector for arduino
Tested on an Arduino Leonardo, but it should work for all
author: r3cursive
*/

int numBuzzers = 10;
int buzzerPins[10] = {0,1,2,3,4,5,6,7,8,9};
unsigned long buzzerTimeDelay = 5000;
long randNumber;

void preAppend(int num)
{
    for (int start = 0; start < num; start++) {
        Serial.print('-');
    }
}

void winner(int num)
{
    Serial.println(num);
    delay(buzzerTimeDelay);
}

void setup() {
    for(int i=0; i < numBuzzers; i++ ) {
        pinMode(buzzerPins[i],INPUT_PULLUP);
    }
    Serial.begin(9600);
}

void loop(){
    for(int i=0; i < numBuzzers; i++ ) {
        if (! digitalRead(buzzerPins[i]) ) {
            //preAppend(random(1,15));
            winner(buzzerPins[i]);
        }
    }   
}