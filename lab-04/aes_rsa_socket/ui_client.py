import sys
import socket
import threading
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class ClientSignals(QObject):
    log_signal = pyqtSignal(str)

class ClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-RSA Socket Client")
        self.resize(550, 420)
        self.setStyleSheet("""
            QWidget { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                font-size: 13px; 
                background-color: #0f172a; 
                color: #f8fafc; 
            }
            QTextEdit, QLineEdit { 
                background: #1e293b; 
                border: 1px solid #334155; 
                border-radius: 6px; 
                padding: 10px; 
                color: #e2e8f0; 
            }
            QTextEdit { font-family: Consolas, monospace; }
            QTextEdit:focus, QLineEdit:focus { border: 1px solid #10b981; }
            
            QPushButton { 
                background-color: #10b981; 
                color: white; 
                border: none; 
                border-radius: 6px; 
                padding: 10px; 
                font-weight: bold; 
            }
            QPushButton:hover { background-color: #059669; }
            QPushButton:disabled { background-color: #475569; color: #94a3b8; }
            QLabel.footer { color: #94a3b8; font-style: italic; font-size: 12px; margin-top: 5px; }
            QLabel.title { font-size: 14px; font-weight: bold; color: #34d399; margin-bottom: 2px; }
        """)
        
        self.signals = ClientSignals()
        self.signals.log_signal.connect(self.log)
        
        self.socket = None
        self.session_key = os.urandom(16)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        lb_title = QLabel("Client Chat Console:")
        lb_title.setProperty("class", "title")
        layout.addWidget(lb_title)
        
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)
        
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a secure message...")
        self.input_field.returnPressed.connect(self.send_msg)
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_msg)
        self.send_btn.setFixedWidth(80)
        self.send_btn.setCursor(Qt.PointingHandCursor)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)
        
        self.connect_btn = QPushButton("Connect to Server")
        self.connect_btn.setCursor(Qt.PointingHandCursor)
        self.connect_btn.clicked.connect(self.connect_server)
        layout.addWidget(self.connect_btn)
        
        footer = QLabel("Sinh viên thực hiện: Trần Quốc Vũ - MSSV: 2380614820")
        footer.setProperty("class", "footer")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        self.input_field.setEnabled(False)
        self.send_btn.setEnabled(False)
        
    def log(self, message):
        if message == "START_UI":
            self.input_field.setEnabled(True)
            self.send_btn.setEnabled(True)
            self.connect_btn.setText("Connected Securely")
            self.input_field.setFocus()
        else:
            self.chat_area.append(message)
            
    def connect_server(self):
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Connecting...")
        threading.Thread(target=self.run_connection, daemon=True).start()
        
    def run_connection(self):
        host = '127.0.0.1'
        port = 12345
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            
            server_pub_bytes = self.socket.recv(2048)
            server_pub_key = serialization.load_pem_public_key(server_pub_bytes)
            
            enc_session_key = server_pub_key.encrypt(
                self.session_key,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            self.socket.send(enc_session_key)
            
            self.signals.log_signal.emit("Connected to Server securely via AES-RSA Hybrid Exchange!")
            self.signals.log_signal.emit("START_UI")
            
        except Exception as e:
            self.signals.log_signal.emit(f"Connection failed: {e}")
            self.connect_btn.setEnabled(True)
            self.connect_btn.setText("Retry Connection")
            
    def send_msg(self):
        text = self.input_field.text().strip()
        if text and self.socket:
            self.chat_area.append(f"<span style='color:#a7f3d0'><b>Me:</b></span> {text}")
            self.input_field.clear()
            
            try:
                cipher = AES.new(self.session_key, AES.MODE_CBC)
                iv = cipher.iv
                ciphertext = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
                self.socket.send(iv + ciphertext)
            except Exception as e:
                self.chat_area.append(f"Error sending msg: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
