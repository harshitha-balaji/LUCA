/*
 * ==========================================================
 * Robot Control
 * ==========================================================
 *
 * Implements high-level robot actions and dispatches
 * commands received from the communication protocol.
 */

#include "robot.h"

#include <ArduinoJson.h>
#include <string.h>

#include "command_constants.h"
#include "firmware_config.h"
#include "servos.h"

static RobotState currentState = RobotState::IDLE;

void initializeRobot()
{
    initializeServos();
    currentState = RobotState::IDLE;
}

RobotState getRobotState()
{
    return currentState;
}

bool executeCommand(const JsonDocument& document)
{
    const char* command = document["cmd"];

    if (strcmp(command, CMD_HOME) == 0)
    {
        homeRobot();
        return true;
    }

    if (strcmp(command, CMD_MOVE) == 0)
    {
        moveRobot(
            document["base"],
            document["shoulder"],
            document["elbow"],
            document["wrist_pitch"],
            document["wrist_roll"],
            document["gripper"]
        );

        return true;
    }

    if (strcmp(command, CMD_STOP) == 0)
    {
        stopRobot();
        return true;
    }

    if (strcmp(command, CMD_GRIPPER_OPEN) == 0)
    {
        openGripper();
        return true;
    }

    if (strcmp(command, CMD_GRIPPER_CLOSE) == 0)
    {
        closeGripper();
        return true;
    }

    return false;
}

void moveRobot(
    int base,
    int shoulder,
    int elbow,
    int wristPitch,
    int wristRoll,
    int gripper
)
{
    currentState = RobotState::MOVING;

    const JointAngles angles{
        base,
        shoulder,
        elbow,
        wristPitch,
        wristRoll,
        gripper
    };

    moveRobotServos(angles);

    currentState = RobotState::IDLE;
}

void homeRobot()
{
    currentState = RobotState::MOVING;

    homeServos();

    currentState = RobotState::IDLE;
}

void stopRobot()
{
    currentState = RobotState::STOPPED;
}

void openGripper()
{
    openGripperServo();
}

void closeGripper()
{
    closeGripperServo();
}