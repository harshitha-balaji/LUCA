from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
)

from PyQt6.QtCore import (
    QTimer,
)

from PyQt6.QtGui import (
    QImage,
    QPixmap,
)

import cv2

from .styles import APP_STYLE
from .widgets.cards import Card

from .components.camera import CameraComponent
from .components.overview import OverviewComponent
from .components.mission import MissionComponent
from .components.event_log import EventLogComponent

from core.robot_controller import RobotController
from .workers.mission_worker import MissionWorker

from PyQt6.QtGui import QIcon

from config import WINDOW_TITLE, ICON_PATH



class MainWindow(QMainWindow):

    IDLE = "IDLE"
    RUNNING = "RUNNING"

    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(str(ICON_PATH)))
        self.resize(1400, 850)
        self.setMinimumSize(1100, 700)

        self.setStyleSheet(APP_STYLE)

        self.state = self.IDLE

        # Backend controller
        self.controller = RobotController()

        #mission worker thread for running missions in the background
        self.mission_worker = None

        # Tracks which backend log events have already
        # been displayed in the UI.
        self._last_log_index = 0

        self._init_ui()
        self._wire_logic()

        # Live camera update timer
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(
            self._update_camera_feed
        )
        self.camera_connected = False
        self.camera_timer.start(33)

        # Synchronize initial UI
        self._update_ui_state()

        # Initial robot message
        self.controller.logger.system("Robot is ready.")
        self._sync_logs()        
        

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
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 0)

        layout.addWidget(header, 0, 0, 1, 2)

        layout.addWidget(self.overview_card, 1, 0)
        layout.addWidget(self.camera_card, 1, 1, 2, 1)
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
    # LOGGING SYNCHRONIZATION
    # ==========================================================

    def _sync_logs(self):
        """
        Synchronize new backend logger events with the UI event log.

        Only events that have not already been displayed are added.
        """

        events = self.controller.logger.get_events()

        new_events = events[self._last_log_index:]

        for event in new_events:

            if event.level.value == "SYSTEM":
                self.log.system(event.message)

            elif event.level.value == "INFO":
                self.log.info(event.message)

            elif event.level.value == "SUCCESS":
                self.log.success(event.message)

            elif event.level.value == "WARNING":
                self.log.warning(event.message)

            elif event.level.value == "ERROR":
                self.log.error(event.message)

        self._last_log_index = len(events)

    # ==========================================================
    # ROBOT ACTIONS
    # ==========================================================

    def start_mission(self):

        if (self.mission_worker is not None and self.mission_worker.isRunning()):
            return
        

        try:
            destination = self.mission.get_destination()

        except ValueError:

            self.controller.logger.warning(
                "Please enter valid destination coordinates before starting a mission."
            )

            self.state = self.IDLE
            self._update_ui_state()

            self._sync_logs()

            return

        self.mission_worker = MissionWorker(
            self.controller,
            destination,
        )

        self.mission_worker.mission_started.connect(
            self._on_mission_started
        )

        self.mission_worker.mission_finished.connect(
            self._on_mission_finished
        )

        self.mission_worker.mission_failed.connect(
            self._on_mission_failed
        )

        self.mission_worker.start()


    def stop_mission(self):
        """
        Stop the robotic arm and reset the UI state.
        """

        success = self.controller.stop()

        if success:
            self.state = self.IDLE
            self._update_ui_state()

        self._sync_logs()

    def home_robot(self):
        """
        Request the robot controller to move the arm
        to its home position.
        """

        self.controller.home()
        self._update_ui_state()

        self._sync_logs()

    def calibrate_workspace(self):
        """
        Capture and store the workspace background image
        for object detection calibration.
        """

        self.controller.calibrate_workspace()
        self._update_ui_state()

        self._sync_logs()

    # ==========================================================
    # MISSION WORKER CALLBACKS
    # ==========================================================

    def _on_mission_started(self):
        """
        Invoked when the mission worker begins execution.
        """

        self.state = self.RUNNING
        self._update_ui_state()

    def _on_mission_finished(self):
        self.state = self.IDLE

        self.mission_worker = None

        self._update_ui_state()
        self._sync_logs()

    def _on_mission_failed(self, message):
        self.state = self.IDLE

        self.controller.logger.error(message)

        self.mission_worker = None

        self._update_ui_state()
        self._sync_logs()
        
    # ==========================================================
    # STATE SYNCHRONIZATION
    # ==========================================================

    def _update_ui_state(self):
        """
        Synchronize all UI components with the current backend state.

        No logging or side effects belong here.
        """

        running = self.state == self.RUNNING


        # Camera is considered connected if a frame is available.
        camera_connected = self.camera_connected

        # ESP32 connection status is determined by the backend controller.
        esp32_connected = self.controller.is_connected()

        # Arm connection status is determined by the backend controller.
        arm_status = self.controller.get_arm_status()

        self.overview.update_status(
            running=running,
            camera_connected=camera_connected,
            esp32_connected=esp32_connected,
            arm_status=arm_status,
        )

        self.mission.set_running_state(running)

    # ==========================================================
    # HELPERS
    # ==========================================================

    def _header_label(self):
        label = QLabel("Modular Robotic Arm System")
        label.setObjectName("mainHeader")
        return label
    
    # ==========================================================
    # CAMERA
    # ==========================================================

    def _update_camera_feed(self):
        """
        Update the live camera feed displayed in the UI.
        """

        frame = self.controller.get_camera_frame()

        self.camera_connected = frame is not None
        self._update_ui_state()

        if frame is None:
            self.camera.clear()
            return

        # Convert OpenCV BGR image to RGB
        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        height, width, channels = frame.shape

        bytes_per_line = channels * width

        image = QImage(
            frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888,
        )

        pixmap = QPixmap.fromImage(image)

        self.camera.set_frame(pixmap)

