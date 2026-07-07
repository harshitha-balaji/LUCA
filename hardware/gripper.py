from communication import SerialInterface


class Gripper:
    """
    High-level interface for controlling the robot gripper.

    This class provides simple methods to open and close
    the gripper while hiding communication details.
    """

    def __init__(self, serial: SerialInterface):
        self.serial = serial

    def open(self):
        """
        Open the robot gripper.

        Returns:
            bool: True if the command was sent successfully,
                  False otherwise.
        """

        return self.serial.send_command({
            "cmd": "gripper_open"
        })

    def close(self):
        """
        Close the robot gripper.

        Returns:
            bool: True if the command was sent successfully,
                  False otherwise.
        """

        return self.serial.send_command({
            "cmd": "gripper_close"
        })