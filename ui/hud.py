import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QColor, QPalette

class JarvisHUD(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window flags for a transparent, stay-on-top overlay
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Geometry: Position at the top right or center
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.status_label = QLabel("SYSTEM IDLE")
        self.status_label.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: #00ffff;") # Cyan JARVIS color

        self.output_label = QLabel("Waiting for input...")
        self.output_label.setFont(QFont("Consolas", 10))
        self.output_label.setStyleSheet("color: #00ffff;")
        self.output_label.setWordWrap(True)

        layout.addWidget(self.status_label)
        layout.addWidget(self.output_label)
        self.setLayout(layout)

    def update_status(self, text):
        self.status_label.setText(text.upper())

    def update_output(self, text):
        self.output_label.setText(text)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hud = JarvisHUD()
    hud.show()
    sys.exit(app.exec())
