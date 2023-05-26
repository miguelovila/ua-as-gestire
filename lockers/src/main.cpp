#include <Arduino.h>
#include <Keypad.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Relay pin definitions
#define LOCKER_1A 13
#define LOCKER_1B 14
#define LOCKER_1C 27
#define LOCKER_1D 26
#define LOCKER_2A 25
#define LOCKER_2B 33
#define LOCKER_2C 32
#define LOCKER_2D 23

// Keypad pin definitions
#define KB_BLACK 15
#define KB_WHITE 4
#define KB_GRAY 16
#define KB_PURPLE 17
#define KB_BLUE 5
#define KB_GREEN 18
#define KB_YELLOW 19

// Keypad setup
char keys[4][3] = {{'1', '2', '3'}, {'4', '5', '6'}, {'7', '8', '9'}, {'*', '0', '#'}};
byte pin_rows[4] = {KB_BLACK, KB_WHITE, KB_GRAY, KB_PURPLE};
byte pin_column[3] = {KB_BLUE, KB_GREEN, KB_YELLOW};
Keypad keypad = Keypad( makeKeymap(keys), pin_rows, pin_column, 4, 3);

// LCD setup
LiquidCrystal_I2C lcd(0x27,20,4);

void setup() {
  // Relay pin setup
  pinMode(LOCKER_1A, OUTPUT);
  pinMode(LOCKER_1B, OUTPUT);
  pinMode(LOCKER_1C, OUTPUT);
  pinMode(LOCKER_1D, OUTPUT);
  pinMode(LOCKER_2A, OUTPUT);
  pinMode(LOCKER_2B, OUTPUT);
  pinMode(LOCKER_2C, OUTPUT);
  pinMode(LOCKER_2D, OUTPUT);
  digitalWrite(LOCKER_1A, HIGH);
  digitalWrite(LOCKER_1B, HIGH);
  digitalWrite(LOCKER_1C, HIGH);
  digitalWrite(LOCKER_1D, HIGH);
  digitalWrite(LOCKER_2A, HIGH);
  digitalWrite(LOCKER_2B, HIGH);
  digitalWrite(LOCKER_2C, HIGH);
  digitalWrite(LOCKER_2D, HIGH);
  // LCD setup
  lcd.init();
  lcd.backlight();
  // Serial setup
  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();

  if (key) {
    Serial.println(key);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Locker ");
    lcd.print(key);
    if (key == '1') {
      digitalWrite(LOCKER_1A, LOW);
      delay(1000);
      digitalWrite(LOCKER_1A, HIGH);
    } else if (key == '2') {
      digitalWrite(LOCKER_1B, LOW);
      delay(1000);
      digitalWrite(LOCKER_1B, HIGH);
    } else if (key == '3') {
      digitalWrite(LOCKER_1C, LOW);
      delay(1000);
      digitalWrite(LOCKER_1C, HIGH);
    } else if (key == '4') {
      digitalWrite(LOCKER_1D, LOW);
      delay(1000);
      digitalWrite(LOCKER_1D, HIGH);
    } else if (key == '5') {
      digitalWrite(LOCKER_2A, LOW);
      delay(1000);
      digitalWrite(LOCKER_2A, HIGH);
    } else if (key == '6') {
      digitalWrite(LOCKER_2B, LOW);
      delay(1000);
      digitalWrite(LOCKER_2B, HIGH);
    } else if (key == '7') {
      digitalWrite(LOCKER_2C, LOW);
      delay(1000);
      digitalWrite(LOCKER_2C, HIGH);
    } else if (key == '8') {
      digitalWrite(LOCKER_2D, LOW);
      delay(1000);
      digitalWrite(LOCKER_2D, HIGH);
    }
  }
}
