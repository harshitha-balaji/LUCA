"""
Computer vision subsystem.

This package provides camera access and object detection
for the robotic arm.
"""

from .camera import Camera
from .detector import Detector

__all__ = [
    "Camera",
    "Detector",
]