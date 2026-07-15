"""
Camera interface for the robotic arm vision system.

This module provides a hardware abstraction over a USB webcam
using OpenCV. It is responsible solely for camera initialization,
frame acquisition, and resource management.

Responsibilities:
- Open the configured camera
- Capture image frames
- Release camera resources

This module does not perform:
- Object detection
- Image processing
- Coordinate estimation
- Robot control
"""

from threading import Lock

import cv2
from numpy import ndarray

from config import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_FPS,
)


class Camera:
    """
    Hardware abstraction for a USB webcam.

    The Camera class is responsible for managing the lifecycle of
    the webcam and providing image frames to the vision subsystem.

    The camera is not opened during initialization. Call `start()`
    to begin capturing frames and `stop()` to release the device.
    """

    def __init__(self) -> None:
        """
        Initialize the camera interface.

        The camera is created in an inactive state.
        """

        self._capture = None
        self._running = False
        self._lock = Lock()

    def start(self) -> None:
        """
        Open and configure the camera.

        Raises:
            RuntimeError: If the camera cannot be opened.
        """

        with self._lock:

            if self._running:
                return

            self._capture = cv2.VideoCapture(CAMERA_INDEX)

            if not self._capture.isOpened():
                self._capture.release()
                self._capture = None
                raise RuntimeError("Failed to open the camera.")

            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
            self._capture.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

            self._running = True

    def stop(self) -> None:
        """
        Release the camera and free its resources.

        If the camera is not running, this method has no effect.
        """

        with self._lock:

            if not self._running:
                return

            self._capture.release()
            self._capture = None
            self._running = False

    def capture_frame(self) -> ndarray:
        """
        Capture and return a single frame from the camera.

        Returns:
            The captured image as an OpenCV frame.

        Raises:
            RuntimeError: If the camera is not running or a frame
                cannot be captured.
        """

        with self._lock:

            if not self._running:
                raise RuntimeError("Camera is not running.")

            success, frame = self._capture.read()

            if not success:
                raise RuntimeError(
                    "Failed to capture a frame from the camera."
                )

            return frame

    @property
    def is_running(self) -> bool:
        """
        Whether the camera is currently active.

        Returns:
            True if the camera has been started, otherwise False.
        """

        with self._lock:
            return self._running