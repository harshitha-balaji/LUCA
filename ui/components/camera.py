from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


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

        self._build_ui()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.feed_label = QLabel(
            "Waiting for camera...\n\n"
            "Connect the robot to begin."
        )

        self.feed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feed_label.setObjectName("supportText")

        layout.addWidget(self.feed_label)

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def set_placeholder(self, text: str):
        """
        Update the placeholder text.

        Used before a live camera stream exists.
        """
        self.feed_label.setText(text)

    def set_frame(self, pixmap):
        """
        Future backend hook.

        Will display incoming camera frames.
        """
        self.feed_label.setPixmap(pixmap)

    def clear(self):
        """
        Return to the idle placeholder.
        """
        self.feed_label.setPixmap(None)
        self.feed_label.setText(
            "Waiting for camera...\n\n"
            "Connect the robot to begin."
        )