/*
 * ==========================================================
 * Servo Control
 * ==========================================================
 *
 * Implements low-level control of the robot servos.
 *
 * Responsibilities:
 * - Initialize servos
 * - Move individual servos
 * - Move the robot to a target joint configuration
 * - Move the robot to its home position
 *
 * This module does not contain:
 * - JSON parsing
 * - Robot logic
 * - Inverse kinematics
 */

#include "servos.h"

#include <Arduino.h>

#include "firmware_config.h"

// ==========================================================
// Servo Objects
// ==========================================================

static Servo baseServo;
static Servo shoulderServo;
static Servo elbowServo;
static Servo wristPitchServo;
static Servo wristRollServo;
static Servo gripperServo;


// ==========================================================
// Helper Functions
// ==========================================================

/*
 * Attach a servo to the specified GPIO pin.
 *
 * If the pin is negative, the servo is not attached.
 * This allows the firmware to compile before the
 * hardware pin assignments have been finalized.
 */
static void attachServo(
    Servo& servo,
    int pin
)
{
    if (pin >= 0)
    {
        servo.attach(pin);
    }
}


// ==========================================================
// Public Interface
// ==========================================================

void initializeServos()
{
    attachServo(baseServo, BASE_SERVO_PIN);
    attachServo(shoulderServo, SHOULDER_SERVO_PIN);
    attachServo(elbowServo, ELBOW_SERVO_PIN);
    attachServo(wristPitchServo, WRIST_PITCH_SERVO_PIN);
    attachServo(wristRollServo, WRIST_ROLL_SERVO_PIN);
    attachServo(gripperServo, GRIPPER_SERVO_PIN);

    homeServos();
}


void moveServo(
    Servo& servo,
    int targetAngle
)
{
    targetAngle = constrain(
        targetAngle,
        SERVO_MIN_ANGLE,
        SERVO_MAX_ANGLE
    );

    servo.write(targetAngle);
}


void moveRobotServos(
    const JointAngles& angles
)
{
    moveServo(baseServo, angles.base);
    delay(SERVO_STEP_DELAY_MS);

    moveServo(shoulderServo, angles.shoulder);
    delay(SERVO_STEP_DELAY_MS);

    moveServo(elbowServo, angles.elbow);
    delay(SERVO_STEP_DELAY_MS);

    moveServo(wristPitchServo, angles.wristPitch);
    delay(SERVO_STEP_DELAY_MS);

    moveServo(wristRollServo, angles.wristRoll);
    delay(SERVO_STEP_DELAY_MS);

    moveServo(gripperServo, angles.gripper);
}


void homeServos()
{
    const JointAngles homeAngles{
        BASE_HOME,
        SHOULDER_HOME,
        ELBOW_HOME,
        WRIST_PITCH_HOME,
        WRIST_ROLL_HOME,
        GRIPPER_HOME
    };

    moveRobotServos(homeAngles);
}

void openGripperServo()
{
    moveServo(
        gripperServo,
        SERVO_MAX_ANGLE
    );
}

void closeGripperServo()
{
    moveServo(
        gripperServo,
        SERVO_MIN_ANGLE
    );
}