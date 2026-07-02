"""
Shared data models for the robotic arm software.

This module defines the common data structures shared between
the GUI, Robot Controller, Vision, Motion, and Hardware modules.

Design Principles:
- Data only (no business logic)
- Lightweight and dependency-free
- Shared across multiple modules
"""

from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Position:
    """
    Represents a point in the robot's 3D workspace.

    All coordinates are expressed in millimeters (mm) relative
    to the robot's base coordinate system.

    Attributes:
        x: Position along the X-axis.
        y: Position along the Y-axis.
        z: Position along the Z-axis.
    """

    x: float
    y: float
    z: float

@dataclass(frozen=True)
class DetectedObject:
    """
    Represents an object detected by the vision system.

    Attributes:
        position: Estimated 3D position of the detected object
                  in the robot's workspace.
    """

    position: Position

@dataclass(frozen=True)
class JointAngles:
    """
    Represents the configuration of the robot's joints.

    This is the output of inverse kinematics and is used by the
    hardware layer to actuate the robotic arm.

    All values are in degrees.
    """

    base: float
    shoulder: float
    elbow: float
    wrist_pitch: float
    wrist_roll: float
    gripper: float

class RobotStatus(Enum):
    """
    Represents the overall operational state of the robot.

    This status reflects the robot's health and readiness,
    independent of the current mission.
    """

    DISCONNECTED = "Disconnected"
    READY = "Ready"
    MOVING = "Moving"
    ERROR = "Error"


class MissionState(Enum):
    """
    Represents the current stage of an autonomous mission.

    This state tracks the progress of the pick-and-place
    workflow from start to completion.
    """

    IDLE = "Idle"
    SEARCHING = "Searching"
    PICKING = "Picking"
    PLACING = "Placing"
    COMPLETED = "Completed"
    FAILED = "Failed"