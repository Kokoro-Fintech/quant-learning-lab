# Purpose: to toggle on and off external screens so Mac doesn't use GPU while plugged in
# Not Working

import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt

class DisplayToggle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Display Toggle Control")
        self.setFixedSize(250, 80)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Display 1")
        self.label.setFixedWidth(70)

        # Sliding switch styled QCheckBox
        self.toggle = QCheckBox()
        self.toggle.setFixedSize(60, 28)
        self.toggle.setStyleSheet('''
            QCheckBox::indicator {
                width: 60px;
                height: 28px;
            }
            QCheckBox::indicator:unchecked {
                image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="60" height="28"><rect width="60" height="28" rx="14" ry="14" fill="#ccc"/></svg>);
            }
            QCheckBox::indicator:checked {
                image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="60" height="28"><rect width="60" height="28" rx="14" ry="14" fill="#4cd964"/><circle cx="40" cy="14" r="12" fill="white"/></svg>);
            }
        ''')
        self.toggle.stateChanged.connect(self.toggle_display)

        layout.addWidget(self.label)
        layout.addWidget(self.toggle)

        self.setLayout(layout)

    def toggle_display(self, state):
        if state == Qt.Checked:
            # Toggle ON: Disable display via displayplacer
            self.run_displayplacer_disable()
        else:
            # Toggle OFF: Enable display via displayplacer
            self.run_displayplacer_enable()
    diplay1_id = "C06257F5-1BC6-451C-B3E9-06995EC2E2C3"
    def run_displayplacer_disable(self):
        # Replace this with your actual displayplacer command to disable the display
        # Example command disables display 1 by setting resolution off (change IDs accordingly)
        cmd = 'displayplacer "id:<display1_id> res:off"'
        print("Disabling display:", cmd)
        subprocess.run(cmd, shell=True)

    def run_displayplacer_enable(self):
        # Replace this with your actual command to restore resolution and enable display
        # Example command restores display 1 to 1920x1080 resolution at 60Hz (change IDs accordingly)
        cmd = 'displayplacer "id:<display1_id> res:1920x1080 hz:60 color_depth:8 scaling:on"'
        print("Enabling display:", cmd)
        subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DisplayToggle()
    window.show()
    sys.exit(app.exec_())
