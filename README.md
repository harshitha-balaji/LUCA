# 🤖 V1 Modular Robotic Arm Controller

A modular desktop application for controlling a 6-DOF robotic arm with integrated vision, motion computation, hardware abstraction, and mission monitoring.

The system is designed around a layered architecture where each subsystem has a clearly defined responsibility, allowing individual modules to be developed, tested, and extended independently.

The controller supports autonomous pick-and-place workflows by combining:

- Real-time camera perception
- Object detection
- Motion computation
- Hardware abstraction
- ESP32-based embedded control
- Interactive PyQt6 dashboard

---

# Project Architecture

```text
robotic_arm/

│
├── main.py
├── config.py
│
├── ui/
│   ├── components/
│   │   ├── camera.py
│   │   ├── event_log.py
│   │   ├── mission.py
│   │   └── overview.py
│   │
│   ├── widgets/
│   │   └── cards.py
│   │
│   ├── workers/
│   │   └── mission_worker.py
│   │
│   ├── styles.py
│   ├── theme.py
│   ├── theme_light.py
│   └── main_window.py
│
├── core/
│   ├── robot_controller.py
│   ├── logger.py
│   └── models.py
│
├── vision/
│   ├── assets/
│   │   └── workspace_background.png
│   │
│   ├── camera.py
│   └── detector.py
│
├── motion/
│   └── kinematics.py
│
├── hardware/
│   ├── arm.py
│   └── gripper.py
│
├── communication/
│   └── serial_interface.py
│
└── firmware/
    └── firmware.ino
```

---

# System Architecture

```
                 User
                  |
                  v
          PyQt6 Dashboard
                  |
                  v
          Robot Controller
                  |
     -------------------------
     |           |           |
     v           v           v
  Vision      Motion      Hardware
 System       System     Abstraction
     |           |           |
     v           v           v
 Camera      Kinematics   Serial Interface
                             |
                             v
                           ESP32
                             |
                             v
                         Robot Hardware
```

---

# Folder Responsibilities

# main.py

Application entry point.

Responsible for:

- Creating the Qt application
- Initializing the main window
- Starting the desktop controller interface

---

# config.py

Central configuration module.

Stores global parameters such as:

- Camera configuration
- Serial communication settings
- Robot parameters
- Vision thresholds
- Workspace configuration

Keeping configuration separate allows hardware and software parameters to be modified without changing application logic.

---

# ui/

Contains all desktop interface components.

The UI layer is responsible only for:

- Displaying robot information
- Receiving user commands
- Showing mission status
- Visualizing camera output and logs

The UI **never directly communicates with hardware**.

All actions are forwarded through the robot controller.

---

## ui/components/

Contains independent dashboard modules.

Current components:

### camera.py

Displays:

- Live camera feed
- Vision status
- Calibration state


### overview.py

Provides a summary of the robot state.

Displays:

- Connection status
- Current robot mode
- Mission state


### mission.py

Handles mission interaction.

Responsible for:

- Starting missions
- Stopping missions
- Displaying mission progress


### event_log.py

Displays system activity.

Includes:

- Robot events
- Mission updates
- Errors
- Debug information

---

## ui/widgets/

Reusable UI building blocks.

Current widgets:

### cards.py

Provides reusable card-style containers used throughout the dashboard.

Future widgets can be added here without affecting individual components.

---
## workers/

Background worker threads used to execute long-running operations without blocking the graphical interface.

Current workers include:

### mission_worker.py

executes autonomous missions on a separate Qt thread, keeping the UI responsive during robot 

operation.
---
## styles.py

Single source of truth for UI design constants.

Contains:

- Colors
- Typography
- Spacing
- Border radius
- Component dimensions

---

## theme.py

Dark theme implementation.

---

## theme_light.py

Light theme implementation.

---

## main_window.py

Main application container.

Responsible for:

- Creating the dashboard layout
- Loading UI components
- Connecting UI events to controller actions


---

# core/

Contains the central application logic.

The core layer coordinates all subsystems.

It does not directly implement:

- Image processing
- Servo control
- Serial communication
- Mathematical calculations

Instead, it orchestrates specialized modules.

---


## robot_controller.py

High-level robot coordinator.

Responsibilities:

- Managing robot state
- Starting and stopping missions
- Coordinating vision results
- Requesting motion calculations
- Sending commands to hardware
- Updating application status

The controller acts as the bridge between the UI and lower-level systems.

---

## models.py

Shared data structures.

Examples:

- Position
- JointAngles
- RobotStatus
- MissionState
- DetectedObject

Models provide consistent communication between modules.

---

## logger.py

Lightweight application event logger.

Responsible for:

- Recording application events
- Categorizing log messages by severity
- Maintaining an in-memory event history
- Providing thread-safe access for the UI

The logger is shared across the application and serves as the backend for the Event Log panel.

---

# vision/

Computer vision subsystem.

Responsible for perception only.

No robot movement logic exists inside this module.

---

## camera.py

Handles:

- Camera initialization
- Frame capture
- Live frame streaming

---

## detector.py

Object detection pipeline.

Current approach:

1. Capture workspace image
2. Compare against calibrated background
3. Apply image processing
4. Detect object contours
5. Estimate object centroid position

---

## assets/

Stores vision calibration resources.

Currently contains:

- Workspace background image captured during calibration and used for background subtraction-based object detection.

---

# motion/

Mathematical motion subsystem.

Currently contains:

## kinematics.py

Responsible for:

- Forward kinematics
- Inverse kinematics
- Coordinate transformations

Input:

```
Target Position
```

Output:

```
Joint Angles
```

The motion layer is independent of the physical robot hardware.

---

# hardware/

Hardware abstraction layer.

Provides high-level robot operations.

The rest of the application interacts with the robot through this layer instead of directly controlling actuators.

---

## arm.py

Controls robotic arm movement.

Provides operations such as:

- Move joints
- Move to position
- Home robot
- Stop movement

---

## gripper.py

Controls gripper operations.

Responsible for:

- Opening gripper
- Closing gripper
- Monitoring grip state

---

# communication/

Communication interface between software and embedded controller.

---

## serial_interface.py

Current communication method:

```
Python Application
        |
      Serial
        |
       ESP32
```

Responsible for:

- Sending commands
- Receiving responses
- Managing communication state

The architecture allows future communication methods:

- USB
- Wi-Fi
- Ethernet
- Bluetooth

without changing higher-level software.

---

# firmware/

Embedded software running on ESP32.

## firmware.ino

Responsible for:

- Receiving commands
- Servo control
- Sensor reading
- Hardware safety handling
- Returning robot status

---

# V1 Workflow

The current target workflow is autonomous pick-and-place.

```
1. Capture workspace image

2. Detect object

3. Estimate object position

4. Compute joint angles

5. Send movement commands

6. Move robotic arm

7. Activate gripper

8. Pick object

9. Move to destination

10. Release object

11. Return to idle state
```

---

# Design Principles

This project follows modular software engineering principles:

- Separation of concerns
- Hardware abstraction
- Single responsibility
- Loose coupling
- Reusable components
- Independent subsystem testing
- Scalable architecture

Each module owns a specific responsibility, allowing improvements without rewriting the complete system.

---

# Future Development

Planned improvements:

- Background camera processing thread
- Dedicated communication thread
- Real-time robot state synchronization
- Advanced trajectory planning
- Collision avoidance
- Object tracking
- AI-based object recognition
- Multi-camera support
- ROS integration
- Remote robot control

---

# Technology Stack

| Component | Technology |
|---|---|
| Desktop UI | PyQt6 |
| Vision Processing | OpenCV |
| Communication | Serial |
| Controller Logic | Python |
| Embedded Controller | ESP32 |
| Firmware | Arduino C++ |

---

# Project Goal

The goal of V1 is to establish a reliable modular foundation for robotic manipulation.

The architecture is designed so future capabilities such as intelligent perception, advanced planning, and autonomous decision-making can be added without redesigning the entire system.