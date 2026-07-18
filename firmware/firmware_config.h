#ifndef FIRMWARE_CONFIG_H
#define FIRMWARE_CONFIG_H

/*
 * ==========================================================
 * Firmware Configuration
 * ==========================================================
 *
 * Hardware-specific configuration.
 *
 * Update these values after final wiring
 * has been completed.
 */

// ==========================================================
// Servo GPIO Pins
// ==========================================================

constexpr int BASE_SERVO_PIN = -1;
constexpr int SHOULDER_SERVO_PIN = -1;
constexpr int ELBOW_SERVO_PIN = -1;
constexpr int WRIST_PITCH_SERVO_PIN = -1;
constexpr int WRIST_ROLL_SERVO_PIN = -1;
constexpr int GRIPPER_SERVO_PIN = -1;


// ==========================================================
// Home Position
// ==========================================================

constexpr int BASE_HOME = 90;
constexpr int SHOULDER_HOME = 90;
constexpr int ELBOW_HOME = 90;
constexpr int WRIST_PITCH_HOME = 90;
constexpr int WRIST_ROLL_HOME = 90;
constexpr int GRIPPER_HOME = 0;


// ==========================================================
// Servo Limits
// ==========================================================

constexpr int SERVO_MIN_ANGLE = 0;
constexpr int SERVO_MAX_ANGLE = 180;

constexpr int SERVO_STEP_DELAY_MS = 150;


#endif