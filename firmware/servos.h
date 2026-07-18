#ifndef SERVOS_H
#define SERVOS_H

/*
 * ==========================================================
 * Servo Control Interface
 * ==========================================================
 *
 * Provides low-level control over the robot servos.
 *
 * Responsibilities:
 * - Initialize servos
 * - Move individual servos
 * - Move the robot to a target joint configuration
 * - Move the robot to its home position
 *
 * This module does not:
 * - Parse JSON
 * - Process robot commands
 * - Perform inverse kinematics
 */

#include <ESP32Servo.h>

struct JointAngles
{
    int base;
    int shoulder;
    int elbow;
    int wristPitch;
    int wristRoll;
    int gripper;
};

void initializeServos();

void moveServo(
    Servo& servo,
    int targetAngle
);

void moveRobotServos(
    const JointAngles& angles
);

void homeServos();

void openGripperServo();

void closeGripperServo();

#endif