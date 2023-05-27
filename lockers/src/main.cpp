#include <Arduino.h>
#include "WiFi.h"
#include <HTTPClient.h>
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

// WiFi configs
const char* ssid = "gestire-demo";
const char* password = "gestiregestire";
IPAddress local_IP(192, 168, 0, 3);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(192, 168, 0, 1);
IPAddress secondaryDNS(1, 1, 1, 1);

// API configs
const char* api_token = "secret1";

// Keypad configs
char keys[4][3] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};
byte pin_rows[4] = {KB_BLACK, KB_WHITE, KB_GRAY, KB_PURPLE};
byte pin_column[3] = {KB_BLUE, KB_GREEN, KB_YELLOW};
Keypad keypad = Keypad( makeKeymap(keys), pin_rows, pin_column, 4, 3);

// LCD configs
LiquidCrystal_I2C lcd(0x27,20,4);

// State machine
enum State {
    S_IDLE,
    S_PROCESSING,
    S_GET,
    S_PUT,
    S_ERROR
};
State state = S_IDLE;

void setup() {
  delay(4000);Serial.begin(115200);
  Serial.println("[INFO] Starting Locker System");

  Serial.println("[INFO] Setting up pins");
  pinMode(LOCKER_1A, OUTPUT); digitalWrite(LOCKER_1A, HIGH);
  pinMode(LOCKER_1B, OUTPUT); digitalWrite(LOCKER_1B, HIGH);
  pinMode(LOCKER_1C, OUTPUT); digitalWrite(LOCKER_1C, HIGH);
  pinMode(LOCKER_1D, OUTPUT); digitalWrite(LOCKER_1D, HIGH);
  pinMode(LOCKER_2A, OUTPUT); digitalWrite(LOCKER_2A, HIGH);
  pinMode(LOCKER_2B, OUTPUT); digitalWrite(LOCKER_2B, HIGH);
  pinMode(LOCKER_2C, OUTPUT); digitalWrite(LOCKER_2C, HIGH);
  pinMode(LOCKER_2D, OUTPUT); digitalWrite(LOCKER_2D, HIGH);
  Serial.println("[INFO] Pins setup done");

  Serial.println("[INFO] Setting up LCD");
  lcd.init(); lcd.backlight();
  Serial.println("[INFO] LCD setup done");

  Serial.println("[INFO] Setting up IP");
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
      Serial.println("[ERROR] Failed to configure IP");
  }
  
  Serial.print("[INFO] Setting up WiFi");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("."); delay(500);
  }
  Serial.println("\n[INFO] WiFi connected");

  Serial.print("[INFO] IP address: ");
  Serial.println(WiFi.localIP());

  Serial.println("[INFO] Setup done");
}

void loop() {
  char key = keypad.getKey();
  if (key) {
    if (key == '1') {
        Serial.println("[INFO] Sending GET request to API");
        HTTPClient http;
    http.begin("http://192.168.0.100:5000");
    int httpCode = http.GET();
    if (httpCode > 0) {
        String payload = http.getString();
        Serial.println(httpCode);
        Serial.println(payload);
      }
    else {
      Serial.println("Error on HTTP request");
    }
    http.end();
    }
  }
}
