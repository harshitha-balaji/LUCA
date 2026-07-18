/*
 * ==========================================================
 * Communication Protocol
 * ==========================================================
 *
 * Handles serial communication between the desktop
 * application and the ESP32.
 *
 * Responsibilities:
 * - Initialize serial communication
 * - Receive JSON commands
 * - Parse incoming messages
 * - Dispatch robot commands
 * - Send status responses
 */

#include "protocol.h"

#include <ArduinoJson.h>

#include "command_constants.h"
#include "robot.h"

void initializeProtocol()
{
    Serial.begin(115200);

    while (!Serial)
    {
        // Wait for the serial port to initialize.
    }
}

void processIncomingCommands()
{
    if (!Serial.available())
    {
        return;
    }

    String message = Serial.readStringUntil('\n');

    StaticJsonDocument<256> document;

    DeserializationError error =
        deserializeJson(document, message);

    if (error)
    {
        StaticJsonDocument<128> response;

        response["status"] = "error";
        response["message"] = "Invalid JSON";

        serializeJson(response, Serial);
        Serial.println();

        return;
    }

    const char* command = document["cmd"];

    if (command == nullptr)
    {
        StaticJsonDocument<128> response;

        response["status"] = "error";
        response["message"] = "Missing command";

        serializeJson(response, Serial);
        Serial.println();

        return;
    }

    if (executeCommand(document))
    {
        StaticJsonDocument<128> response;

        response["status"] = "ok";

        serializeJson(response, Serial);
        Serial.println();
    }
    else
    {
        StaticJsonDocument<128> response;

        response["status"] = "error";
        response["message"] = "Unknown command";

        serializeJson(response, Serial);
        Serial.println();
    }
}