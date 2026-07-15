"""
Communication interfaces.

This package provides communication channels used by the
robot controller.
"""

from .serial_interface import SerialInterface

__all__ = ["SerialInterface"]