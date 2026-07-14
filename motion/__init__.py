"""
Motion planning and inverse kinematics.

This package provides motion-related algorithms used by the
robot controller.
"""

from .kinematics import InverseKinematics

__all__ = ["InverseKinematics"]