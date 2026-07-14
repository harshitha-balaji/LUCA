from communication import SerialInterface
from core.models import JointAngles


class Arm:
    """
    High-level interface for controlling the robotic arm.

    This class translates robot actions into commands
    that are sent to the ESP32 through the SerialInterface.
    """

    def __init__(self, serial: SerialInterface):
        self.serial = serial

    def home(self):
        """
        Send the robot to its home position.

        Returns:
            bool: True if the command was sent successfully,
                  False otherwise.
        """

        return self.serial.send_command({
            "cmd": "home"
        })
    
    def move_to_angles(self, angles: JointAngles):
        """
        Move the robotic arm to the specified joint angles.

        Args:
            angles (JointAngles):
                Target joint configuration.

        Returns:
            bool:
                True if the command was sent successfully,
                False otherwise.
        """

        command = {
            "cmd": "move",
            "base": angles.base,
            "shoulder": angles.shoulder,
            "elbow": angles.elbow,
            "wrist_pitch": angles.wrist_pitch,
            "wrist_roll": angles.wrist_roll,
            "gripper": angles.gripper
        }

        return self.serial.send_command(command)
    
    def stop(self):
        """
        Stop all robot motion immediately.

        Returns:
            bool: True if the command was sent successfully,
                False otherwise.
        """

        return self.serial.send_command({
            "cmd": "stop"
        })
    
    def get_status(self):
        """
        Request the current robot status.

        Returns:
            dict | None:
                Robot status received from the ESP32.
        """

        if not self.serial.send_command({
            "cmd": "status"
        }):
            return None

        return self.serial.read_response()
    
    