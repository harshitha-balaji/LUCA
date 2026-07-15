from communication import SerialInterface

from hardware import (Arm,Gripper)

from motion import InverseKinematics

from vision import (Camera,Detector)

from core.logger import Logger
from core.models import Position


import cv2
from config import BACKGROUND_IMAGE_PATH

class RobotController:
    """
    Coordinates the robotic arm subsystems.

    This class acts as the bridge between the user interface
    and the robot backend.
    """

    def __init__(self):

        # Log
        self.logger = Logger()

        # Communication
        self.serial = SerialInterface()

        # Hardware
        self.arm = Arm(self.serial)
        self.gripper = Gripper(self.serial)

        # Motion
        self.ik = InverseKinematics()

        # Vision
        self.camera = Camera()
        self.detector = Detector()

        # Mission control
        self._stop_requested = False

    # ==========================================================
    # COMMUNICATION
    # ==========================================================

    def connect(self, port: str) -> bool:
        """
        Connect to the robotic arm.

        Args:
            port:
                Serial port of the ESP32.

        Returns:
            True if the connection was established successfully,
            otherwise False.
        """

        self.logger.info(f"Attempting to connect to {port}.")

        success = self.serial.connect(port)

        if success:
            self.logger.success(f"Connected to {port}.")
        else:
            self.logger.error(f"Failed to connect to {port}.")

        return success


    def disconnect(self) -> None:
        """
        Disconnect from the robotic arm.

        If no active connection exists, this method has no effect.
        """

        if not self.is_connected():
            self.logger.warning("Robot is already disconnected.")
            return

        port = self.serial.port

        self.logger.info(f"Disconnecting from {port}.")

        self.serial.disconnect()

        self.logger.success(f"Disconnected from {port}.")


    def is_connected(self) -> bool:
        """
        Check whether the robotic arm is currently connected.

        Returns:
            True if the robot is connected, otherwise False.
        """

        return self.serial.is_connected()


    def get_log_events(self):
        """
        Return the application event history.

        Returns:
            A copy of the recorded log events.
        """

        return self.logger.get_events()
    
    # ==========================================================
    # ROBOT CONTROL COMMANDS
    # ==========================================================

    def home(self) -> bool:
        """
        Move the robot arm to its predefined home position.
        """

        self.logger.info(
            "Moving the arm to its home position."
        )

        success = self.arm.home()

        if success:
            self.logger.success(
                "The arm is back at its home position and ready."
            )
        else:
            self.logger.error(
                "I couldn't move the arm home right now. "
                "The robot is safe, but the connection should be checked."
            )

        return success
    
    def stop(self) -> bool:
        """
        Stop all robotic arm motion immediately.
        """
        self._stop_requested = True

        self.logger.warning(
            "Stopping robotic arm motion."
        )

        success = self.arm.stop()

        if success:
            self.logger.success(
                "The robotic arm has been stopped safely."
            )
        else:
            self.logger.error(
                "Failed to stop the robotic arm. "
                "The connection should be checked."
            )

        return success
    
    def calibrate_workspace(self) -> bool:
        """
        Capture and store an empty workspace image for
        object detection calibration.
        """

        self.logger.info(
            "Calibrating the robot workspace."
        )

        try:

            if not self.camera.is_running:
                self.camera.start()

            frame = self.camera.capture_frame()

            cv2.imwrite(
                BACKGROUND_IMAGE_PATH,
                frame,
            )

            self.detector.set_background(
                frame
            )

            self.logger.success(
                "Workspace calibration completed successfully."
            )

            return True

        except Exception as error:

            self.logger.error(
                "I couldn't calibrate the workspace. "
                f"{error}"
            )

            return False
    
    
    def start_mission(
        self,
        destination: Position,
    ) -> bool:
        """
        Execute an autonomous pick-and-place mission.

        Args:
            destination:
                Target location where the detected object
                should be placed.

        Returns:
            True if the mission completed successfully,
            otherwise False.
        """
        self._stop_requested = False

        self.logger.info(
            "Starting the autonomous pick-and-place mission."
        )

        try:

            # ------------------------------------------
            # Ensure camera is running
            # ------------------------------------------

            if not self.camera.is_running:
                self.camera.start()
            

            # ------------------------------------------
            # Detect object
            # ------------------------------------------

            self.logger.info(
                "Searching the workspace for an object."
            )

            frame = self.camera.capture_frame()

            detected_object = self.detector.detect(
                frame
            )

            if detected_object is None:

                self.logger.warning(
                    "I couldn't find any object in the workspace."
                )

                return False

            self.logger.success(
                "An object has been detected in the workspace."
            )

            if self._should_stop():
                return False

            # ------------------------------------------
            # Plan robot motion
            # ------------------------------------------

            self.logger.info(
                "Planning the path to the object."
            )

            pickup_angles = self.ik.solve(
                detected_object.position
            )

            self.logger.success(
                "A valid robot motion has been planned."
            )

            if self._should_stop():
                return False

            # ------------------------------------------
            # Move to object
            # ------------------------------------------

            self.logger.info(
                "Moving to the detected object."
            )

            if not self.arm.move_to_angles(
                pickup_angles
            ):

                self.logger.error(
                    "I couldn't move the robot to the detected object."
                )

                return False

            self.logger.success(
                "The robot has reached the object."
            )

            if self._should_stop():
                return False

            # ------------------------------------------
            # Pick object
            # ------------------------------------------

            self.logger.info(
                "Picking the detected object."
            )

            if not self.gripper.close():

                self.logger.error(
                    "I couldn't secure the detected object."
                )

                return False

            self.logger.success(
                "The object has been secured."
            )

            if self._should_stop():
                return False

            # ------------------------------------------
            # Plan motion to destination
            # ------------------------------------------

            self.logger.info(
                "Planning the path to the destination."
            )

            place_angles = self.ik.solve(
                destination
            )

            self.logger.success(
                "A valid robot motion has been planned."
            )

            if self._should_stop():
                return False

            # ------------------------------------------
            # Move to destination
            # ------------------------------------------

            self.logger.info(
                "Moving to the destination."
            )

            if not self.arm.move_to_angles(
                place_angles
            ):

                self.logger.error(
                    "I couldn't move the robot to the destination."
                )

                return False

            self.logger.success(
                "The robot has reached the destination."
            )

            if self._should_stop():
                return False

            # ------------------------------------------
            # Release object
            # ------------------------------------------

            self.logger.info(
                "Releasing the object."
            )

            if not self.gripper.open():

                self.logger.error(
                    "I couldn't release the object."
                )

                return False

            self.logger.success(
                "The object has been placed successfully."
            )

            self.logger.success(
                "The pick-and-place mission has completed successfully."
            )

            return True

        except Exception as error:

            self.logger.error(
                "I couldn't complete the pick-and-place mission. "
                f"{error}"
            )

            return False
        
    # ==========================================================
    # MISSION HELPERS
    # ==========================================================

    def _should_stop(self) -> bool:
        """
        Check whether the current mission has been cancelled.
        """

        if self._stop_requested:
            self.logger.warning(
                "Mission cancelled by the user."
            )
            return True

        return False
        
    # ==========================================================
    # CAMERA CONTROL
    # ==========================================================

    def get_camera_frame(self):
        """
        Capture and return the latest camera frame.

        This method is intended for the graphical user interface
        to display a live camera feed. If the camera has not yet
        been started, it is initialized automatically.

        Returns:
            The latest camera frame if available,
            otherwise None.
        """

        try:

            if not self.camera.is_running:
                self.camera.start()

            return self.camera.capture_frame()

        except Exception:

            return None
        
    def get_arm_status(self):

        status = self.arm.get_status()

        if status is None:
            return "Unknown"

        return status.get("state", "Unknown")

