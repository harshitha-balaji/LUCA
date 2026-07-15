from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class CameraComponent(QWidget):
    """
    Camera Feed Component

    Responsible for displaying the robot's camera feed.

    V1:
        • Idle placeholder
        • Future-ready API for backend integration

    V2:
        • Live camera stream
        • Detection overlays
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._current_pixmap = None

        self._build_ui()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.feed_label = QLabel(
            "📷\n\n"
            "Camera is standing by.\n\n"
            "Start a mission or calibrate the workspace\n"
            "to begin the live camera feed."
        )

        self.feed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feed_label.setScaledContents(False)
        self.feed_label.setObjectName("supportText")

        # Ignore the pixmap's natural size when computing layouts.
        self.feed_label.setSizePolicy(
            QSizePolicy.Policy.Ignored,
            QSizePolicy.Policy.Ignored,
        )

        layout.addWidget(self.feed_label)

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def set_placeholder(self, text: str):
        """
        Update the placeholder text.

        Used before a live camera stream exists.
        """

        self._current_pixmap = None

        self.feed_label.clear()
        self.feed_label.setText(text)

    def set_frame(self, pixmap: QPixmap):
        """
        Display a camera frame.
        """

        self._current_pixmap = pixmap
        self.feed_label.setText("")

        self._update_pixmap()

    def clear(self):
        """
        Return to the idle placeholder.
        """

        self._current_pixmap = None

        self.feed_label.clear()
        self.feed_label.setText(
            "📷\n\n"
            "Camera Offline\n\n"
            "Press Calibrate or Start Mission\n"
            "to initialize the vision system."
        )

    # -------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------

    def _update_pixmap(self):
        """
        Scale the current frame to fit the available space
        while preserving its aspect ratio.
        """

        if self._current_pixmap is None:
            return

        scaled = self._current_pixmap.scaled(
            self.feed_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.feed_label.setPixmap(scaled)

    # -------------------------------------------------
    # Events
    # -------------------------------------------------

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self._update_pixmap()