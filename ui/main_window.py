from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
)

from .styles import APP_STYLE
from .widgets.cards import Card

from .components.camera import CameraComponent
from .components.overview import OverviewComponent
from .components.mission import MissionComponent
from .components.event_log import EventLogComponent


class MainWindow(QMainWindow):

    IDLE = "IDLE"
    RUNNING = "RUNNING"

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modular Robotic Arm Controller")
        self.resize(1400, 850)
        self.setMinimumSize(1100, 700)

        self.setStyleSheet(APP_STYLE)

        self.state = self.IDLE

        self._init_ui()
        self._wire_logic()

        # Synchronize initial UI
        self._update_ui_state()

        # Initial robot message
        self.log.system("Robot is ready.")

    # ==========================================================
    # UI ASSEMBLY
    # ==========================================================

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QGridLayout(central)
        layout.setSpacing(14)
        layout.setContentsMargins(14, 14, 14, 14)

        # ---------------- Header ----------------

        header = Card("Robot Controller")
        header.add_widget(self._header_label())

        # ---------------- Overview ----------------

        self.overview_card = Card("Robot Overview")
        self.overview = OverviewComponent()
        self.overview_card.add_widget(self.overview)

        # ---------------- Mission ----------------

        self.mission_card = Card("Mission Controls")
        self.mission = MissionComponent()
        self.mission_card.add_widget(self.mission)

        # ---------------- Camera ----------------

        self.camera_card = Card("Camera Feed")
        self.camera = CameraComponent()
        self.camera_card.add_widget(self.camera)

        # ---------------- Event Log ----------------

        self.log_card = Card("Event Log")
        self.log = EventLogComponent()
        self.log_card.add_widget(self.log)

        # ---------------- Layout ----------------

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 3)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 1)

        layout.addWidget(header, 0, 0, 1, 2)

        layout.addWidget(self.overview_card, 1, 0)
        layout.addWidget(self.camera_card, 1, 1)

        layout.addWidget(self.mission_card, 2, 0)

        layout.addWidget(self.log_card, 3, 0, 1, 2)

    # ==========================================================
    # CALLBACK WIRING
    # ==========================================================

    def _wire_logic(self):
        self.mission.bind_actions(
            start_cb=self.start_mission,
            home_cb=self.home_robot,
            calibrate_cb=self.calibrate_workspace,
            stop_cb=self.stop_mission,
        )

    # ==========================================================
    # ROBOT ACTIONS
    # ==========================================================

    def start_mission(self):

        if self.state == self.RUNNING:
            return

        self.state = self.RUNNING
        self._update_ui_state()

        # Simulated mission sequence
        self.log.system("Mission started.")
        self.log.info("Planning motion...")
        self.log.info("Moving to target...")
        self.log.success("Object detected.")
        self.log.info("Moving to pick position...")
        self.log.info("Object grasped.")
        self.log.info("Moving to destination...")
        self.log.info("Object released.")
        self.log.system("Mission complete.")

        self.state = self.IDLE
        self._update_ui_state()

        self.log.system("Ready for the next mission.")

    def stop_mission(self):

        self.state = self.IDLE
        self._update_ui_state()

        self.log.warning("Mission stopped by user.")
        self.log.system("Ready for the next mission.")

    def home_robot(self):
        self.log.system("Homing robot...")

    def calibrate_workspace(self):
        self.log.system("Calibrating workspace...")
        self.log.success("Workspace calibration complete.")

    # ==========================================================
    # STATE SYNCHRONIZATION
    # ==========================================================

    def _update_ui_state(self):
        """
        Synchronize visual state only.

        No logging or side effects belong here.
        """

        running = self.state == self.RUNNING

        self.overview.set_running(running)
        self.mission.set_running_state(running)

    # ==========================================================
    # HELPERS
    # ==========================================================

    def _header_label(self):
        label = QLabel("Modular Robotic Arm System")
        label.setObjectName("mainHeader")
        return label

