#include <Arduino.h>
#include "WiFi.h"
#include <HTTPClient.h>
#include <Keypad.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

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
const char *ssid = "gestire-demo";
const char *password = "gestiregestire";
IPAddress local_IP(192, 168, 0, 3);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(192, 168, 0, 1);
IPAddress secondaryDNS(1, 1, 1, 1);

// API configs
const char *API_URL = "http://192.168.0.100:5000/api";
const char *API_SECRET = "farto_da_papelada_de_analise_de_sistemas";

// Keypad configs
char keys[4][3] = {
    {'1', '2', '3'},
    {'4', '5', '6'},
    {'7', '8', '9'},
    {'*', '0', '#'}};
byte pin_rows[4] = {KB_BLACK, KB_WHITE, KB_GRAY, KB_PURPLE};
byte pin_column[3] = {KB_BLUE, KB_GREEN, KB_YELLOW};
Keypad keypad = Keypad(makeKeymap(keys), pin_rows, pin_column, 4, 3);

// LCD configs
LiquidCrystal_I2C lcd(0x27, 20, 4);

// State machine
enum State
{
    S_IDLE,
    S_INPUT,
    S_ABORTED,
    S_PROCESSING,
    S_INVALID,
    S_GET,
    S_PUT,
    S_ERROR
};
State state = S_IDLE;

char *locker;

void setup()
{
    delay(1000);
    Serial.begin(115200);
    Serial.println("[INFO] Starting Locker System");

    Serial.println("[INFO] Setting up pins");
    pinMode(LOCKER_1A, OUTPUT);
    digitalWrite(LOCKER_1A, HIGH);
    pinMode(LOCKER_1B, OUTPUT);
    digitalWrite(LOCKER_1B, HIGH);
    pinMode(LOCKER_1C, OUTPUT);
    digitalWrite(LOCKER_1C, HIGH);
    pinMode(LOCKER_1D, OUTPUT);
    digitalWrite(LOCKER_1D, HIGH);
    pinMode(LOCKER_2A, OUTPUT);
    digitalWrite(LOCKER_2A, HIGH);
    pinMode(LOCKER_2B, OUTPUT);
    digitalWrite(LOCKER_2B, HIGH);
    pinMode(LOCKER_2C, OUTPUT);
    digitalWrite(LOCKER_2C, HIGH);
    pinMode(LOCKER_2D, OUTPUT);
    digitalWrite(LOCKER_2D, HIGH);
    Serial.println("[INFO] Pins setup done");

    Serial.println("[INFO] Setting up LCD");
    lcd.init();
    lcd.backlight();
    Serial.println("[INFO] LCD setup done");

    Serial.println("[INFO] Setting up IP");
    if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS))
    {
        Serial.println("[ERROR] Failed to configure IP");
    }

    Serial.print("[INFO] Setting up WiFi");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(500);
    }
    Serial.println("\n[INFO] WiFi connected");

    Serial.print("[INFO] IP address: ");
    Serial.println(WiFi.localIP());

    Serial.println("[INFO] Setup done");
}

char code[7] = "------";

void loop()
{
    switch (state)
    {
    case S_IDLE:
    {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print(" Gestire Locker ");
        lcd.setCursor(0, 1);
        lcd.print(" Type your code ");

        for (int i = 0; i < 6; i++)
        {
            code[i] = '-';
        }
        delete[] locker;

        while (1)
        {
            char key = keypad.getKey();
            if (key && key != '#' && key != '*')
            {
                code[0] = key;
                state = S_INPUT;
                break;
            }
        }
    }
    break;
    case S_INPUT:
    {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print(" Type your code ");
        lcd.setCursor(5, 1);
        for (int i = 0; i < 6; i++)
        {
            lcd.print(code[i]);
        }
        int i = 1;
        while (i < 6)
        {
            char key = keypad.getKey();
            if (key)
            {
                if (key == '#')
                {
                    state = S_ABORTED;
                    break;
                }
                else if (key == '*')
                {
                    if (i > 0)
                    {
                        i--;
                        code[i] = '-';
                        lcd.setCursor(5 + i, 1);
                        lcd.print(code[i]);
                    }
                    continue;
                }
                code[i] = key;
                lcd.setCursor(5 + i, 1);
                lcd.print(code[i]);
                i++;
            }
        }
        if (state != S_ABORTED)
        {
            state = S_PROCESSING;
        }
    }
    break;
    case S_ABORTED:
    {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("   Operation    ");
        lcd.setCursor(0, 1);
        lcd.print("      aborted   ");
        delay(5000);
        state = S_IDLE;
    }
    break;
    case S_PROCESSING:
    {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("  Processing    ");
        lcd.setCursor(0, 1);
        lcd.print("     operation  ");

        // Send post request to API with a JSON containing the api secret
        HTTPClient http;
        char url[50];
        snprintf(url, sizeof(url), "%s/locker/%s", API_URL, code);

        const size_t capacity = JSON_OBJECT_SIZE(1) + 30;
        DynamicJsonDocument jsonDoc(capacity);
        jsonDoc["token"] = API_SECRET;

        String jsonPayload;
        serializeJson(jsonDoc, jsonPayload);

        http.begin(url);
        http.addHeader("Content-Type", "application/json");
        int httpResponseCode = http.POST(jsonPayload);

        if (httpResponseCode > 0)
        {
            String payload = http.getString();
            Serial.println(httpResponseCode);
            Serial.println(payload);
            if (httpResponseCode == 400)
            {
                state = S_INVALID;
            }
            else if (httpResponseCode == 200)
            {
                const size_t capacity = JSON_OBJECT_SIZE(2) + 30;
                DynamicJsonDocument jsonDoc(capacity);
                deserializeJson(jsonDoc, payload);
                const char *type = jsonDoc["type"];
                const char *lockerValue = jsonDoc["locker"];
                locker = new char[strlen(lockerValue) + 1];
                strcpy(locker, lockerValue);
                if (strcmp(type, "put") == 0)
                {
                    state = S_PUT;
                }
                else if (strcmp(type, "get") == 0)
                {
                    state = S_GET;
                }
                else
                {
                    state = S_ERROR;
                }
            }
            else
            {
                state = S_ERROR;
            }
        }
        else
        {
            Serial.println("Error on HTTP request");
            state = S_ERROR;
        }
        delay(2000);
    }
    break;
    case S_PUT:
    {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("  Return it to  ");
        lcd.setCursor(0, 1);
        lcd.print("       ");
        lcd.print(locker);
        delay(10000);
        state = S_IDLE;
    }
    break;
    case S_GET:
    {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("  Take it from  ");
        lcd.setCursor(0, 1);
        lcd.print("       ");
        lcd.print(locker);
        delay(10000);
        state = S_IDLE;
    }
    break;
    case S_ERROR:
    {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("   Operation    ");
        lcd.setCursor(0, 1);
        lcd.print("       failed   ");
        delay(3000);
        state = S_IDLE;
    }
    break;
    case S_INVALID:
    {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("    Invalid     ");
        lcd.setCursor(0, 1);
        lcd.print("        code    ");
        delay(3000);
        state = S_IDLE;
    }
    default:
        break;
    }
}
