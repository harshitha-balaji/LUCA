from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from core.models import Position


class MissionComponent(QWidget):
    """
    Mission Controls Component

    Responsible only for collecting mission inputs and
    exposing user actions. Styling is handled globally.
    """

    def __init__(self):
        super().__init__()

        self._build_ui()

        self.start_cb = None
        self.home_cb = None
        self.calibrate_cb = None
        self.stop_cb = None

        self.start_btn.clicked.connect(self._start)
        self.home_btn.clicked.connect(self._home)
        self.calibrate_btn.clicked.connect(self._calibrate)
        self.stop_btn.clicked.connect(self._stop)

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        section = QLabel("Destination Coordinates")
        section.setObjectName("supportText")
        layout.addWidget(section)

        self.x = QLineEdit()
        self.y = QLineEdit()
        self.z = QLineEdit()

        self.x.setPlaceholderText("X (mm)")
        self.y.setPlaceholderText("Y (mm)")
        self.z.setPlaceholderText("Z (mm)")

        layout.addWidget(self.x)
        layout.addWidget(self.y)
        layout.addWidget(self.z)

        # Primary action
        self.start_btn = QPushButton("▶ Start Mission")
        self.start_btn.setObjectName("primaryBtn")
        layout.addWidget(self.start_btn)

        # Secondary actions
        row = QHBoxLayout()
        row.setSpacing(10)

        self.home_btn = QPushButton("⌂ Home Robot")
        self.home_btn.setObjectName("secondaryBtn")

        self.calibrate_btn = QPushButton("⟳ Calibrate")
        self.calibrate_btn.setObjectName("secondaryBtn")

        row.addWidget(self.home_btn)
        row.addWidget(self.calibrate_btn)

        layout.addLayout(row)

        # Danger action
        self.stop_btn = QPushButton("■ Stop Mission")
        self.stop_btn.setObjectName("dangerBtn")
        layout.addWidget(self.stop_btn)

    # -------------------------------------------------
    # Wiring
    # -------------------------------------------------

    def bind_actions(
        self,
        start_cb,
        home_cb,
        calibrate_cb,
        stop_cb,
    ):
        self.start_cb = start_cb
        self.home_cb = home_cb
        self.calibrate_cb = calibrate_cb
        self.stop_cb = stop_cb

    # -------------------------------------------------
    # Internal handlers
    # -------------------------------------------------

    def _start(self):
        if self.start_cb:
            self.start_cb()

    def _home(self):
        if self.home_cb:
            self.home_cb()

    def _calibrate(self):
        if self.calibrate_cb:
            self.calibrate_cb()

    def _stop(self):
        if self.stop_cb:
            self.stop_cb()

    
    def get_destination(self) -> Position:
        """
        Return the destination coordinates entered by the user.

        Returns:
            Position:
                Destination expressed in workspace coordinates.

        Raises:
            ValueError:
                If any coordinate is invalid.
        """

        return Position(
            x=float(self.x.text()),
            y=float(self.y.text()),
            z=float(self.z.text()),
        )

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def set_running_state(self, running: bool):
        """
        Synchronize controls with the robot state.
        """

        self.start_btn.setEnabled(not running)
        self.calibrate_btn.setEnabled(not running)

        # Safe actions remain available.
        self.home_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)