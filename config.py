"""
Global configuration for the Robotic Arm Controller.

This module contains configurable parameters shared across
multiple subsystems. Centralizing these values makes it easy
to adapt the application to different hardware without
modifying the implementation of individual modules.

Current configuration:
- USB camera settings
- Vision detector settings

Future additions:
- Serial communication
- Robot workspace
- Motion parameters
- Default robot positions
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ==========================================================
# Application
# ==========================================================

APP_NAME = "LUCA"

APP_FULL_NAME = "Lightweight Unified Controller Assistant"

APP_VERSION = "1.0.0"

ICON_PATH = BASE_DIR / "assets" / "icon.png"
WINDOW_TITLE = f"{APP_NAME} — {APP_FULL_NAME}"

# ==========================================================
# Camera Configuration
# ==========================================================

# OpenCV camera device index.
# Typical values:
#   0 -> Built-in laptop camera
#   1 -> External USB webcam
CAMERA_INDEX = 0

# Desired camera resolution.
# The webcam will attempt to use these settings if supported.
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# Desired capture frame rate (FPS).
# Actual FPS depends on webcam capabilities.
CAMERA_FPS = 30


# ==========================================================
# Vision Detector Configuration
# ==========================================================

# Path to the stored empty workspace image.
# This image is captured during workspace calibration.

BACKGROUND_IMAGE_PATH = (
    BASE_DIR / "vision" / "assets" / "background.png"
)

# Minimum pixel difference required to consider a pixel
# as part of a detected object.
#
# Higher values:
#   - Reduce sensitivity
#   - Remove small lighting changes
#
# Lower values:
#   - Detect smaller changes
#   - More sensitive to noise
DIFFERENCE_THRESHOLD = 30


# Minimum contour area (pixels²) for a valid object.
MIN_OBJECT_AREA = 400


# Maximum contour area (pixels²) for a valid object.
MAX_OBJECT_AREA = 30000


# Size of the Gaussian blur kernel.
# Used before image comparison to reduce noise.
BLUR_KERNEL_SIZE = (5, 5)


# Size of the morphological kernel used for
# cleaning the foreground mask.
MORPH_KERNEL_SIZE = (5, 5)

# ==========================================================
# Workspace Calibration
# ==========================================================

# Physical dimensions of the robot workspace (millimeters).
#
# These values correspond to the region visible to the camera
# that the robot can safely reach.
WORKSPACE_WIDTH = 300.0
WORKSPACE_HEIGHT = 250.0

# Pixel coordinates of the workspace corners in the camera image.
#
# Order:
#   1. Top-left
#   2. Top-right
#   3. Bottom-right
#   4. Bottom-left
#
# Leave as None until the camera has been mounted and the
# workspace has been calibrated.
WORKSPACE_IMAGE_POINTS = None

# ==========================================================
# Serial Communication
# ==========================================================

# Default serial communication settings.
SERIAL_BAUD_RATE = 115200

SERIAL_TIMEOUT = 1

# ==========================================================
# Robot Geometry (millimetres)
# ==========================================================

BASE_HEIGHT = 100.0

UPPER_ARM_LENGTH = 140.0

FOREARM_LENGTH = 140.0

WRIST_LENGTH = 70.0


# ==========================================================
# Joint Limits (degrees)
# ==========================================================

BASE_MIN = -180.0
BASE_MAX = 180.0

SHOULDER_MIN = -90.0
SHOULDER_MAX = 90.0

ELBOW_MIN = 0.0
ELBOW_MAX = 180.0

WRIST_PITCH_MIN = -90.0
WRIST_PITCH_MAX = 90.0

WRIST_ROLL_MIN = -180.0
WRIST_ROLL_MAX = 180.0

GRIPPER_MIN = 0.0
GRIPPER_MAX = 90.0


