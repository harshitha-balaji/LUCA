from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget


class Card(QFrame):
    def __init__(self, title=""):
        super().__init__()

        self.setObjectName("card")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(14, 12, 14, 14)
        self.main_layout.setSpacing(10)

        self.title = QLabel(title)
        self.title.setObjectName("cardTitle")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(6)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.content_widget)

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)