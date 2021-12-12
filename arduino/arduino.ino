// Incluimos librería
#include <LiquidCrystal.h>
#include <OneWire.h>
#include <DallasTemperature.h>

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

const int  pin1_0 = 34;
const int  pin1_1 = 28;
const int  pin1_2 = 27;
const int  pin1_3 = 31;

const int  pin2_0 = 30;
const int  pin2_1 = 26;

const int  pin3_0 = 36;
const int  pin3_1 = 22;

const int  pin4_0 = 32;

const int pinLDR = A15;

const int pinTimbre = 51;
const int pinBuzz = 9;

const int EchoPin = 12;
const int TriggerPin = 13;

const int oneWirePin = 8;
OneWire oneWireBus(oneWirePin);
DallasTemperature sensor(&oneWireBus);

int tim = 0;

const int ledRojo1 = 47;
const int ledRojo2 = 49;

void setup(){
  lcd.begin(16, 2);
  // Escribimos el Mensaje en el LCD.
  lcd.print("Temperatura: ");
  
  Serial.begin(9600);
  
  pinMode(pin1_0, OUTPUT);
  pinMode(pin1_1, OUTPUT);
  pinMode(pin1_2, OUTPUT);
  pinMode(pin1_3, OUTPUT);

  pinMode(pin2_0, OUTPUT);
  pinMode(pin2_1, OUTPUT);

  pinMode(pin3_0, OUTPUT);
  pinMode(pin3_1, OUTPUT);

  pinMode(pin4_0, OUTPUT);

  pinMode(pinLDR, INPUT);

  pinMode(pinTimbre, INPUT);
  pinMode(pinBuzz, OUTPUT);

  pinMode(TriggerPin, OUTPUT);
  pinMode(EchoPin, INPUT);

  sensor.begin(); 
}

void loop(){
    if (Serial.available()>0) 
   {
      char option = Serial.read();
      
      if (option == '1')
      {
        digitalWrite(pin1_0, HIGH);
        digitalWrite(pin1_1, HIGH);
        digitalWrite(pin1_2, HIGH);
        digitalWrite(pin1_3, HIGH);
      }

      else if (option == '2')
      {
        digitalWrite(pin1_0, LOW);
        digitalWrite(pin1_1, LOW);
        digitalWrite(pin1_2, LOW);
        digitalWrite(pin1_3, LOW);
      }

      else if (option == '3')
      {
        digitalWrite(pin2_0, HIGH);
        digitalWrite(pin2_1, HIGH);
      }

      else if (option == '4')
      {
        digitalWrite(pin2_0, LOW);
        digitalWrite(pin2_1, LOW);
      }

      else if (option == '5')
      {
        digitalWrite(pin3_0, HIGH);
        digitalWrite(pin3_1, HIGH);
      }

      else if (option == '6')
      {
        digitalWrite(pin3_0, LOW);
        digitalWrite(pin3_1, LOW);
      }

      else if (option == '7')
      {
        digitalWrite(pin4_0, HIGH);
      }

      else if (option == '8')
      {
        digitalWrite(pin4_0, LOW);
      }

      else if (option == '9')
      {
        digitalWrite(pin1_0, HIGH);
        digitalWrite(pin1_1, HIGH);
        digitalWrite(pin1_2, HIGH);
        digitalWrite(pin1_3, HIGH);
        digitalWrite(pin2_0, HIGH);
        digitalWrite(pin2_1, HIGH),
        digitalWrite(pin3_0, HIGH);
        digitalWrite(pin3_1, HIGH);
        digitalWrite(pin4_0, HIGH);
      }

      else if (option == '0')
      {
        digitalWrite(pin1_0, LOW);
        digitalWrite(pin1_1, LOW);
        digitalWrite(pin1_2, LOW);
        digitalWrite(pin1_3, LOW);
        digitalWrite(pin2_0, LOW);
        digitalWrite(pin2_1, LOW),
        digitalWrite(pin3_0, LOW);
        digitalWrite(pin3_1, LOW);
        digitalWrite(pin4_0, LOW);
      }

      else if (option == 'a')
      {
          int alarma = 0;
          while (alarma == 0){
            analogWrite(pinBuzz, 155);
            delay(500);
            analogWrite(pinBuzz, 0);
            delay(50);
            analogWrite(pinBuzz, 155);
            delay(500);
            analogWrite(pinBuzz, 0);
            delay(50);
            alarma = digitalRead(pinTimbre);
          }
      }

      else if (option == 'b')
      {
        digitalWrite(ledRojo1, HIGH);
        digitalWrite(ledRojo2, HIGH);
      }

      else if (option == 'c')
      {
        digitalWrite(ledRojo1, LOW);
        digitalWrite(ledRojo2, LOW);
      }
  }

  // VOID LOOP
  int LDR = analogRead(pinLDR);
  String stringLDR = String(LDR);
  
  int cm = ping(TriggerPin, EchoPin);
  String stringCM = String(cm);

  float temp = sensor.getTempCByIndex(0);
  String stringTemp = String(temp);

  sensor.requestTemperatures();
  
  Serial.println(stringLDR + '/' + stringTemp + '/' + stringCM);

  if (digitalRead(pinTimbre) == HIGH) // TIMBRE
  {
    analogWrite(pinBuzz, 155);
    delay(500);
    analogWrite(pinBuzz, 0);
    delay(50);
    analogWrite(pinBuzz, 155);
    delay(500);
    analogWrite(pinBuzz, 0);
    delay(50);
  }

  tim = (millis() / 10000)%10;
  if (tim % 2 != 0){
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Temperatura: ");
    lcd.setCursor(0, 1);
    lcd.print(stringTemp + " C");
  }

  if (tim % 2 == 0) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Nivell de llum: %");
    lcd.setCursor(0, 1);
    lcd.print(LDR/10);
  }
}



// EXTRA FUNCTIONS

int ping(int TriggerPin, int EchoPin) {
   long duration, distanceCm;
   
   digitalWrite(TriggerPin, LOW);  //para generar un pulso limpio ponemos a LOW 4us
   delayMicroseconds(4);
   digitalWrite(TriggerPin, HIGH);  //generamos Trigger (disparo) de 10us
   delayMicroseconds(10);
   digitalWrite(TriggerPin, LOW);
   
   duration = pulseIn(EchoPin, HIGH);  //medimos el tiempo entre pulsos, en microsegundos
   
   distanceCm = duration * 10 / 292/ 2;   //convertimos a distancia, en cm
   return distanceCm;
}
