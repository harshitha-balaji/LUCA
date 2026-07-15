from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout


class OverviewComponent(QWidget):
    """
    Robot Overview Component

    Displays a concise summary of the robot's current state.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # -----------------------------
        # Summary status
        # -----------------------------
        self.status_line = QLabel("● Ready")
        self.status_line.setObjectName("statusReady")
        layout.addWidget(self.status_line)

        # -----------------------------
        # System information
        # -----------------------------
        self.camera_status = QLabel("Unknown")
        self.esp32_status = QLabel("Unknown")
        self.arm_status = QLabel("Unknown")
        self.mode_status = QLabel("Idle")

        layout.addWidget(self._row("Camera", self.camera_status))
        layout.addWidget(self._row("ESP32", self.esp32_status))
        layout.addWidget(self._row("Arm", self.arm_status))
        layout.addWidget(self._row("Mode", self.mode_status))

    def _row(self, label_text: str, value_label: QLabel) -> QWidget:
        container = QWidget()

        row = QGridLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setHorizontalSpacing(10)

        label = QLabel(label_text)
        label.setObjectName("supportText")

        row.addWidget(label, 0, 0)
        row.addWidget(value_label, 0, 1)

        return container

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def update_status(
        self,
        *,
        running: bool,
        camera_connected: bool,
        esp32_connected: bool,
        arm_status: str,
    ):
        """
        Synchronize all overview fields with the backend state.
        """

        # Summary + Mode
        if running:
            self.status_line.setText("● Running")
            self.status_line.setObjectName("statusRunning")
            self.mode_status.setText("Running")
        else:
            self.status_line.setText("● Ready")
            self.status_line.setObjectName("statusReady")
            self.mode_status.setText("Idle")

        self.status_line.style().unpolish(self.status_line)
        self.status_line.style().polish(self.status_line)

        # Camera
        self.camera_status.setText(
            "Connected" if camera_connected else "Disconnected"
        )

        # ESP32
        self.esp32_status.setText(
            "Connected" if esp32_connected else "Disconnected"
        )

        # Arm
        self.arm_status.setText(arm_status)