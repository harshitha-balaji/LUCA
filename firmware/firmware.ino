/*
 * ==========================================================
 * Robotic Arm Controller Firmware
 * ==========================================================
 *
 * Entry point for the ESP32 firmware.
 *
 * Responsibilities:
 * - Initialize hardware
 * - Initialize serial communication
 * - Process incoming commands
 *
 * This file intentionally contains very little logic.
 * Most functionality is delegated to dedicated modules.
 */

#include "robot.h"
#include "protocol.h"

void setup()
{
    initializeProtocol();
    initializeRobot();
}

void loop()
{
    processIncomingCommands();
}