"""
Object detection module for the robotic arm vision system.

This module is responsible for detecting objects within a camera
frame and estimating their positions in the robot's workspace.

Responsibilities:
- Process image frames
- Detect target objects
- Estimate object positions

This module does not perform:
- Camera management
- Robot control
- Motion planning
- Hardware communication
"""

import cv2
import numpy as np
from numpy import ndarray
import os

from config import (
    BLUR_KERNEL_SIZE,
    MORPH_KERNEL_SIZE,
    MIN_OBJECT_AREA,
    MAX_OBJECT_AREA,
    DIFFERENCE_THRESHOLD,
    BACKGROUND_IMAGE_PATH,
    WORKSPACE_WIDTH,
    WORKSPACE_HEIGHT,
    WORKSPACE_IMAGE_POINTS,
)

from core.models import (
    DetectedObject,
    Position,
)

class Detector:
    """
    Detects target objects from camera frames.

    This class encapsulates the computer vision pipeline used
    to locate objects and estimate their positions.

    The detector is independent of the camera source and the
    robot controller. It processes image frames and returns
    detected objects.

    The detection method uses background subtraction, where a
    calibrated empty workspace image is compared against the
    current camera frame.
    """

    def __init__(self) -> None:
        """
        Initialize the object detector.

        Loads detector configuration and prepares resources
        required for image processing.       """        

        self._transform_matrix = self._create_workspace_transform()

        self._min_area = MIN_OBJECT_AREA
        self._max_area = MAX_OBJECT_AREA

        self._difference_threshold = DIFFERENCE_THRESHOLD

        self._blur_kernel_size = BLUR_KERNEL_SIZE

        self._kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            MORPH_KERNEL_SIZE,
        )

        self._background = self._load_background()            

    def set_background(self, frame: ndarray) -> None:
        """
        Store an empty workspace frame for background subtraction.

        This method should be called once during workspace
        calibration.

        Args:
            frame: Image captured from an empty workspace.
        """

        self._background = self._preprocess(frame)

    def detect(self, frame: ndarray) -> DetectedObject | None:
        """
        Detect the largest valid object within a camera frame.

        Args:
            frame: Image captured from the camera.

        Returns:
            The detected object if one is found,
            otherwise None.
        """

        if self._background is None:
            raise RuntimeError(
                "Workspace background has not been calibrated."
            )

        if self._transform_matrix is None:
            raise RuntimeError(
                "Workspace transform has not been calibrated."
            )

        processed_frame = self._preprocess(frame)

        difference = self._compute_difference(
            processed_frame
        )

        mask = self._create_mask(
            difference
        )

        cleaned_mask = self._clean_mask(
            mask
        )

        contour = self._find_largest_contour(
            cleaned_mask
        )

        if contour is None:
            return None

        center = self._compute_center(
            contour
        )

        return self._create_detected_object(
            center
        )
    
    def _create_workspace_transform(self) -> ndarray | None:
        """
        Create the perspective transformation used to convert
        image pixel coordinates into robot workspace coordinates.

        Returns:
            The perspective transformation matrix if workspace
            calibration data is available, otherwise None.
        """

        if WORKSPACE_IMAGE_POINTS is None:
            return None

        image_points = np.array(
            WORKSPACE_IMAGE_POINTS,
            dtype=np.float32,
        )

        workspace_points = np.array(
            [
                [0.0, 0.0],
                [WORKSPACE_WIDTH, 0.0],
                [WORKSPACE_WIDTH, WORKSPACE_HEIGHT],
                [0.0, WORKSPACE_HEIGHT],
            ],
            dtype=np.float32,
        )

        return cv2.getPerspectiveTransform(
            image_points,
            workspace_points,
        )
    
    def _load_background(self) -> ndarray | None:
        """
        Load the previously calibrated workspace background.

        Returns:
            The preprocessed background image if one exists,
            otherwise None.
        """

        if not os.path.exists(BACKGROUND_IMAGE_PATH):
            return None

        background = cv2.imread(BACKGROUND_IMAGE_PATH)

        if background is None:
            return None

        return self._preprocess(background)

    def _preprocess(self, frame: ndarray) -> ndarray:
        """
        Preprocess a camera frame before comparison.

        The preprocessing stage reduces image noise before
        performing background subtraction.

        Args:
            frame: Image captured from the camera.

        Returns:
            The blurred image.
        """

        blurred = cv2.GaussianBlur(
            frame,
            self._blur_kernel_size,
            0,
        )

        return blurred
    
    def _compute_difference(self, frame: ndarray) -> ndarray:
        """
        Compute the difference between the current frame and
        the calibrated workspace background.

        Args:
            frame: Preprocessed current camera frame.

        Returns:
            Absolute difference image.
        """

        difference = cv2.absdiff(
            self._background,
            frame,
        )

        return difference
    
    def _create_mask(self, difference: ndarray) -> ndarray:
        """
        Create a binary foreground mask from the difference image.

        Pixels with a difference greater than the configured
        threshold are considered part of the detected object.

        Args:
            difference: Absolute difference image between the
                        current frame and workspace background.

        Returns:
            Binary foreground mask.
        """

        gray_difference = cv2.cvtColor(
            difference,
            cv2.COLOR_BGR2GRAY,
        )

        _, mask = cv2.threshold(
            gray_difference,
            self._difference_threshold,
            255,
            cv2.THRESH_BINARY,
        )

        return mask
    
    def _clean_mask(self, mask: ndarray) -> ndarray:
        """
        Remove noise and improve the foreground mask.

        Morphological opening removes small isolated pixels,
        while closing fills small gaps inside detected regions.

        Args:
            mask: Binary foreground mask.

        Returns:
            Cleaned binary mask.
        """

        opened = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            self._kernel,
        )

        cleaned = cv2.morphologyEx(
            opened,
            cv2.MORPH_CLOSE,
            self._kernel,
        )

        return cleaned
    
    def _find_largest_contour(
        self,
        mask: ndarray,
    ) -> ndarray | None:
        """
        Find the largest valid contour from the foreground mask.

        Contours are filtered based on configured area limits.
        The largest remaining contour is considered the target object.

        Args:
            mask: Cleaned binary foreground mask.

        Returns:
            The largest valid contour if found, otherwise None.
        """

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        valid_contours = []

        for contour in contours:
            area = cv2.contourArea(contour)

            if self._min_area <= area <= self._max_area:
                valid_contours.append(contour)

        if not valid_contours:
            return None

        largest_contour = max(
            valid_contours,
            key=cv2.contourArea,
        )

        return largest_contour
    
    def _compute_center(
        self,
        contour: ndarray,
    ) -> tuple[int, int]:
        """
        Compute the centroid of a contour.

        Args:
            contour: Object contour detected from the foreground mask.

        Returns:
            The center point as (x, y) pixel coordinates.
        """

        moments = cv2.moments(contour)

        if moments["m00"] == 0:
            return (0, 0)

        center_x = int(
            moments["m10"] / moments["m00"]
        )

        center_y = int(
            moments["m01"] / moments["m00"]
        )

        return center_x, center_y
    
    def _pixel_to_workspace(
        self,
        center: tuple[int, int],
    ) -> Position:
        """
        Convert image pixel coordinates into robot workspace
        coordinates.

        Args:
            center: Object center in image pixel coordinates.

        Returns:
            Position expressed in millimeters within the robot
            workspace.

        Raises:
            RuntimeError: If the workspace has not been calibrated.
        """

        if self._transform_matrix is None:
            raise RuntimeError(
                "Workspace has not been calibrated."
            )

        pixel = np.array(
            [[[center[0], center[1]]]],
            dtype=np.float32,
        )

        world = cv2.perspectiveTransform(
            pixel,
            self._transform_matrix,
        )

        world_x, world_y = world[0][0]

        return Position(
            x=float(world_x),
            y=float(world_y),
            z=0.0,
        )
    
    def _create_detected_object(
        self,
        center: tuple[int, int],
    ) -> DetectedObject:
        """
        Create a DetectedObject from an image pixel coordinate.

        The pixel coordinate is converted into robot workspace
        coordinates before constructing the detected object.

        Args:
            center: Object center as (x, y) image pixel coordinates.

        Returns:
            A detected object with its position expressed in the
            robot workspace.
        """

        position = self._pixel_to_workspace(
            center
        )

        return DetectedObject(
            position=position,
        )
    
    