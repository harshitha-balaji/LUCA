import json
import serial


class SerialInterface:
    """
    Handles serial communication with the ESP32.

    Responsibilities:
    - Connect to the robot
    - Disconnect
    - Send commands
    - Receive responses

    This class does not contain robot logic.
    It only manages communication.
    """

    def __init__(self):
        # Stores the currently connected serial port.
        self.port = None

        # Default communication speed.
        self.baud_rate = 115200

        # Active serial connection object.
        self.connection = None

        # Connection status.
        self.connected = False

    def connect(self, port):
        """
        Establish a serial connection with the ESP32.

        Args:
            port (str): Serial port name (e.g., COM3, COM4).

        Returns:
            bool: True if connected successfully, False otherwise.
        """

        try:
            self.connection = serial.Serial(
                port=port,
                baudrate=self.baud_rate,
                timeout=1
            )

            self.port = port
            self.connected = True

            return True

        except serial.SerialException as error:
            self.connection = None
            self.connected = False

            print(f"Connection Error: {error}")

            return False

    def disconnect(self):
        """
        Close the serial connection.
        """

        if self.connection is not None:
            self.connection.close()

        self.connection = None
        self.connected = False
        self.port = None

    def is_connected(self):
        """
        Check whether the serial interface is connected.

        Returns:
            bool: Connection status.
        """

        return self.connected

    def send_command(self, command: dict):
        """
        Send a JSON command to the ESP32.

        Args:
            command (dict): Command dictionary.

        Returns:
            bool: True if sent successfully, False otherwise.
        """

        if not isinstance(command, dict):
            raise TypeError("Command must be a dictionary.")

        if not self.is_connected():
            return False

        message = json.dumps(command)
        message += "\n"

        try:
            self.connection.write(message.encode("utf-8"))
            return True

        except serial.SerialException as error:
            print(f"Send Error: {error}")
            return False

    def read_response(self):
        """
        Read a JSON response from the ESP32.

        Returns:
            dict | None:
                Parsed JSON response if successful,
                otherwise None.
        """

        if not self.is_connected():
            return None

        try:
            response = self.connection.readline()
            response = response.decode("utf-8").strip()

            # No response received.
            if not response:
                return None

            return json.loads(response)

        except (serial.SerialException, json.JSONDecodeError) as error:
            print(f"Read Error: {error}")
            return None