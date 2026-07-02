from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
)


class EventLogComponent(QWidget):
    """
    Event Log Component

    Displays a chronological story of robot activity.
    """

    INFO = "logInfo"
    SUCCESS = "logSuccess"
    WARNING = "logWarning"
    ERROR = "logError"
    SYSTEM = "logSystem"

    def __init__(self):
        super().__init__()

        self._build_ui()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def _build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        # QScrollArea paints its own background/frame by default, which can
        # mask the themed content widget underneath. Keep it transparent so
        # the QWidget#eventLog rule in styles.py is what actually shows.
        self.scroll.setStyleSheet("background: transparent; border: none;")

        # This is the widget that QWidget#eventLog in styles.py targets.
        # (Previously nothing had this objectName set, so that rule was
        # dead CSS and the log fell back to Qt's default background —
        # which is why it looked "stuck" in dark mode regardless of theme.)
        content = QWidget()
        content.setObjectName("eventLog")

        self.layout = QVBoxLayout(content)
        self.layout.setContentsMargins(14, 12, 14, 14)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(6)

        self.scroll.setWidget(content)

        root.addWidget(self.scroll)

    # -------------------------------------------------
    # Core API
    # -------------------------------------------------

    def add_event(self, message: str, style: str = INFO):

        row = QWidget()
        row_layout = QHBoxLayout(row)

        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(12)

        timestamp = QLabel(datetime.now().strftime("%H:%M"))
        timestamp.setObjectName("logTimestamp")

        text = QLabel(message)
        text.setWordWrap(True)
        text.setObjectName(style)

        row_layout.addWidget(timestamp)
        row_layout.addWidget(text, 1)

        self.layout.addWidget(row)

        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    # -------------------------------------------------
    # Convenience API
    # -------------------------------------------------

    def info(self, message):
        self.add_event(message, self.INFO)

    def success(self, message):
        self.add_event(message, self.SUCCESS)

    def warning(self, message):
        self.add_event(message, self.WARNING)

    def error(self, message):
        self.add_event(message, self.ERROR)

    def system(self, message):
        self.add_event(message, self.SYSTEM)
