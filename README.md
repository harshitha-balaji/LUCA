# 🤖 V1 Modular Robotic Arm Controller

A modular desktop application for controlling a 6-DOF robotic arm capable of autonomous pick-and-place operations.

The project is designed with a clean separation of responsibilities so that each subsystem can be developed, tested, and extended independently.

---

# Project Architecture

```
robotic_arm/

│
├── main.py
├── config.py
│
├── ui/
│   ├── components/
│   ├── widgets/
│   ├── styles.py
│   ├── theme.py
│   ├── theme_light.py
│   └── main_window.py
│
├── core/
│   ├── robot_controller.py
│   └── models.py
│
├── vision/
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

# Folder Responsibilities

## main.py

Application entry point.

Responsible for launching the Qt application and initializing the main window.

---

## config.py

Global project configuration.

Examples include:

- Camera index
- Serial port
- Baud rate
- Workspace limits
- Default robot parameters

---

# ui/

Contains every component related to the desktop interface.

The UI layer **never directly controls hardware**.

It only displays information and forwards user actions to the controller.

### components/

Independent dashboard panels.

Current components include:

- Camera Feed
- Robot Overview
- Mission Control
- Event Log

Each component is self-contained and reusable.

### widgets/

Reusable UI building blocks shared across multiple components.

Examples:

- Cards
- Status indicators
- Future reusable widgets

### styles.py

Single source of truth for:

- Colors
- Fonts
- Spacing
- Border radius
- Design constants

### theme.py

Dark theme implementation.

### theme_light.py

Light theme implementation.

### main_window.py

Creates the application layout and assembles all dashboard components.

---

# core/

Contains the application's central logic.

The controller coordinates communication between every subsystem.

It does **not** perform image processing, inverse kinematics or hardware communication itself.

Instead, it orchestrates those modules.

### robot_controller.py

Responsible for:

- Starting missions
- Handling robot state
- Receiving vision results
- Calling inverse kinematics
- Sending commands to hardware
- Updating UI status

### models.py

Shared data structures used across the project.

Examples include:

- Position
- JointAngles
- RobotStatus
- MissionState
- DetectedObject

---

# vision/

Computer vision subsystem.

Responsible for:

- Capturing camera frames
- Detecting objects
- Estimating object positions

No robot control logic exists here.

---

# motion/

Mathematical motion planning.

Currently contains inverse kinematics calculations.

Input:

- Target position

Output:

- Joint angles

Independent from hardware implementation.

---

# hardware/

Hardware abstraction layer.

Provides high-level robot operations such as:

- Move arm
- Open gripper
- Close gripper
- Home robot

The rest of the application should never directly manipulate servos.

---

# communication/

Handles communication between the desktop application and the robot controller.

Current implementation:

- Serial communication with ESP32

Future communication methods can be added without affecting higher-level code.

Examples:

- USB
- Wi-Fi
- Ethernet
- Bluetooth

---

# firmware/

Embedded software running on the ESP32.

Responsible for:

- Receiving commands
- Driving servos
- Reading sensors
- Returning robot status

---

# Design Principles

This project follows several software engineering principles:

- Separation of concerns
- Modular architecture
- Reusable UI components
- Hardware abstraction
- Loose coupling
- Single responsibility
- Scalable project structure

Each folder owns a single responsibility, making the project easier to understand, maintain and extend.

---

# V1 Scope

The first version focuses on autonomous pick-and-place.

Workflow:

1. Capture camera image
2. Detect object
3. Estimate object position
4. Compute inverse kinematics
5. Send joint commands
6. Move robotic arm
7. Pick object
8. Move to destination
9. Place object
10. Return to idle state

Future versions can build upon this architecture by adding:

- Multiple object tracking
- Motion planning
- Collision avoidance
- AI-based object recognition
- Multi-camera support
- ROS integration
- Remote control
