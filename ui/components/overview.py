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
        layout.addWidget(self._row("Camera", "Connected"))
        layout.addWidget(self._row("ESP32", "Connected"))
        layout.addWidget(self._row("Arm", "Homed"))
        layout.addWidget(self._row("Mode", "Idle"))

    def _row(self, label_text: str, value_text: str) -> QWidget:
        container = QWidget()

        row = QGridLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setHorizontalSpacing(10)

        label = QLabel(label_text)
        label.setObjectName("supportText")

        value = QLabel(value_text)

        row.addWidget(label, 0, 0)
        row.addWidget(value, 0, 1)

        return container

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def set_running(self, running: bool):
        """
        Updates the summary status shown at the top of the card.
        """

        if running:
            self.status_line.setText("● Running")
            self.status_line.setObjectName("statusRunning")
        else:
            self.status_line.setText("● Ready")
            self.status_line.setObjectName("statusReady")

        # Refresh stylesheet after changing object name
        self.status_line.style().unpolish(self.status_line)
        self.status_line.style().polish(self.status_line)