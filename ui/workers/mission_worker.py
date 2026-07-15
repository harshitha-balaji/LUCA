from PyQt6.QtCore import QThread, pyqtSignal
from core.robot_controller import RobotController
from core.models import Position

class MissionWorker(QThread):
    """
    Runs a robot mission in a background thread.

    This keeps the Qt event loop responsive while the
    robotic arm executes a mission.
    """

    mission_started = pyqtSignal()
    mission_finished = pyqtSignal()
    mission_failed = pyqtSignal(str)

    def __init__(self,controller: RobotController,destination: Position):
        super().__init__()

        self.controller = controller
        self.destination = destination

    def run(self):
        """
        Execute the mission.
        """

        self.mission_started.emit()

        try:
            self.controller.start_mission(self.destination)
            self.mission_finished.emit()

        except Exception as e:
            self.mission_failed.emit(str(e))