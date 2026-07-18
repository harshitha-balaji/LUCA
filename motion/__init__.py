"""
Motion planning and inverse kinematics.

This package provides motion-related algorithms used by the
robot controller.
"""

from .kinematics import InverseKinematics
from .trajectory import TrajectoryPlanner

__all__ = ["InverseKinematics"]