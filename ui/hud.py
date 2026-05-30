import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QPen
import psutil

class ArcReactor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)

    def rotate(self):
        self.angle = (self.angle + 5) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Outer ring
        painter.setPen(QPen(QColor(0, 255, 255, 150), 3))
        painter.drawEllipse(10, 10, 80, 80)

        # Inner pulsing ring
        painter.setPen(QPen(QColor(0, 255, 255, 200), 5, Qt.PenStyle.DashLine))
        painter.save()
        painter.translate(50, 50)
        painter.rotate(self.angle)
        painter.drawEllipse(-30, -30, 60, 60)
        painter.restore()

        # Center core
        painter.setBrush(QColor(0, 255, 255, 100))
        painter.drawEllipse(40, 40, 20, 20)

class BiometricSplash(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()
        self.label = QLabel("IDENTITY SCAN IN PROGRESS...")
        self.label.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        self.label.setStyleSheet("color: #00ffff;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.progress = QProgressBar()
        self.progress.setStyleSheet("QProgressBar { border: 2px solid #00ffff; color: #00ffff; text-align: center; } QProgressBar::chunk { background-color: #00ffff; }")
        layout.addWidget(self.progress)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.val = 0
        self.timer.start(30)

    def update_progress(self):
        self.val += 2
        self.progress.setValue(self.val)
        if self.val >= 100:
            self.timer.stop()
            self.label.setText("IDENTITY VERIFIED: WELCOME MR. STARK")
            QTimer.singleShot(1000, self.finish)

    def finish(self):
        self.close()
        self.callback()

class JarvisHUD(QWidget):
    def __init__(self):
        super().__init__()
        self.is_authenticated = False
        self.initUI()
        self.hide() # Hide until splash finishes

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(100, 100, 500, 350)

        main_layout = QVBoxLayout()

        # Header with Arc Reactor and Status
        header_layout = QHBoxLayout()
        self.arc = ArcReactor(self)
        header_layout.addWidget(self.arc)

        status_vbox = QVBoxLayout()
        self.status_label = QLabel("SYSTEM ONLINE")
        self.status_label.setFont(QFont("Consolas", 16, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: #00ffff;")
        status_vbox.addWidget(self.status_label)

        header_layout.addLayout(status_vbox)
        main_layout.addLayout(header_layout)

        # System Stats
        stats_layout = QHBoxLayout()
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setFormat("CPU: %p%")
        self.cpu_bar.setStyleSheet("QProgressBar { border: 1px solid #00ffff; color: #00ffff; text-align: center; } QProgressBar::chunk { background-color: #00ffff; }")

        self.ram_bar = QProgressBar()
        self.ram_bar.setFormat("RAM: %p%")
        self.ram_bar.setStyleSheet("QProgressBar { border: 1px solid #00ffff; color: #00ffff; text-align: center; } QProgressBar::chunk { background-color: #008888; }")

        stats_layout.addWidget(self.cpu_bar)
        stats_layout.addWidget(self.ram_bar)
        main_layout.addLayout(stats_layout)

        # Output Text
        self.output_label = QLabel("Welcome back, Sir.")
        self.output_label.setFont(QFont("Consolas", 11))
        self.output_label.setStyleSheet("color: #00ffff; background: rgba(0, 0, 0, 50); border-radius: 5px; padding: 10px;")
        self.output_label.setWordWrap(True)
        main_layout.addWidget(self.output_label)

        # Log Terminal
        self.log_label = QLabel("> Booting systems...\n> Gemini connection established.")
        self.log_label.setFont(QFont("Consolas", 8))
        self.log_label.setStyleSheet("color: rgba(0, 255, 255, 150);")
        main_layout.addWidget(self.log_label)

        self.setLayout(main_layout)

        # Update stats timer
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(2000)

    def update_stats(self):
        self.cpu_bar.setValue(int(psutil.cpu_percent()))
        self.ram_bar.setValue(int(psutil.virtual_memory().percent))

    def update_status(self, text):
        self.status_label.setText(text.upper())

    def update_output(self, text):
        self.output_label.setText(text)
        self.add_log(f"Response: {text[:30]}...")

    def add_log(self, text):
        current_logs = self.log_label.text().split("\n")
        current_logs.append(f"> {text}")
        if len(current_logs) > 5:
            current_logs = current_logs[-5:]
        self.log_label.setText("\n".join(current_logs))

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
