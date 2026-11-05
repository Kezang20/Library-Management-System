import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QMessageBox
)

class HelloWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Hello World")
        self.setGeometry(400, 200, 400, 250)

        layout = QVBoxLayout()

        self.label = QLabel("Hello World!")
        self.label.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.show_message)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def show_message(self):
        QMessageBox.information(
            self, "Message", "Hello! Welcome to PyQt6."
        )


app = QApplication(sys.argv)
window = HelloWindow()
window.show()
sys.exit(app.exec())