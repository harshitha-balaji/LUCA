#ifndef ROBOT_H
#define ROBOT_H

#include <ArduinoJson.h>

enum class RobotState
{
    IDLE,
    MOVING,
    STOPPED
};

void initializeRobot();

RobotState getRobotState();

bool executeCommand(const JsonDocument& document);

void moveRobot(
    int base,
    int shoulder,
    int elbow,
    int wristPitch,
    int wristRoll,
    int gripper
);

void homeRobot();

void stopRobot();

void openGripper();

void closeGripper();

#endif