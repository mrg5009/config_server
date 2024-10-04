import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

# Function to send knock using nmap
def send_knock(port_sequence, server_ip="45.152.86.73"):
    for port in port_sequence:
        command = f"nmap -p {port} --scanflags SYN {server_ip}"
        os.system(command)

class KnockdGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set up the layout and widgets
        layout = QVBoxLayout()

        self.label = QLabel('Select a service to open or close:')
        layout.addWidget(self.label)

        # Open/Close HTTP Service (Port 8000)
        self.open_http_button = QPushButton('Open HTTP (Port 8000)', self)
        self.open_http_button.clicked.connect(lambda: self.send_predefined_knock("open", "http"))
        layout.addWidget(self.open_http_button)

        self.close_http_button = QPushButton('Close HTTP (Port 8000)', self)
        self.close_http_button.clicked.connect(lambda: self.send_predefined_knock("close", "http"))
        layout.addWidget(self.close_http_button)

        # Open/Close SSH Service (Port 22)
        self.open_ssh_button = QPushButton('Open SSH (Port 22)', self)
        self.open_ssh_button.clicked.connect(lambda: self.send_predefined_knock("open", "ssh"))
        layout.addWidget(self.open_ssh_button)

        self.close_ssh_button = QPushButton('Close SSH (Port 22)', self)
        self.close_ssh_button.clicked.connect(lambda: self.send_predefined_knock("close", "ssh"))
        layout.addWidget(self.close_ssh_button)

        # Open/Close SOCKS5 Service (Port 1080)
        self.open_socks_button = QPushButton('Open SOCKS5 (Port 1080)', self)
        self.open_socks_button.clicked.connect(lambda: self.send_predefined_knock("open", "socks"))
        layout.addWidget(self.open_socks_button)

        self.close_socks_button = QPushButton('Close SOCKS5 (Port 1080)', self)
        self.close_socks_button.clicked.connect(lambda: self.send_predefined_knock("close", "socks"))
        layout.addWidget(self.close_socks_button)

        # Add more services here...

        # Set the layout to the QWidget
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Port Knocker')
        self.setGeometry(300, 300, 400, 200)

    # Function to send knock sequence for predefined services
    def send_predefined_knock(self, action, service):
        sequences = {
            "http": {
                "open": [2000, 2100, 2200],  # Knock sequence to open HTTP (Port 8000)
                "close": [1600, 1700, 1800]  # Knock sequence to close HTTP (Port 8000)
            },
            "ssh": {
                "open": [1000, 1100, 1200],  # Knock sequence to open SSH (Port 22)
                "close": [1300, 1400, 1500]  # Knock sequence to close SSH (Port 22)
            },
            "socks": {
                "open": [3000, 3100, 3200],  # Knock sequence to open SOCKS5 (Port 1080)
                "close": [3300, 3400, 3500]  # Knock sequence to close SOCKS5 (Port 1080)
            },
            # Add more services with their knock sequences here...
        }

        if service in sequences:
            if action in sequences[service]:
                send_knock(sequences[service][action])
                self.show_message("Success", f"{action.capitalize()} sequence sent for {service.upper()}!")
            else:
                self.show_message("Error", f"Invalid action for {service}!")
        else:
            self.show_message("Error", "Service not found!")

    # Function to show messages
    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

# Main entry point for the PyQt6 application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = KnockdGUI()
    gui.show()
    sys.exit(app.exec())
