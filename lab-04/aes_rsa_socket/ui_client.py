import sys
import socket
import threading
import os
import qdarktheme
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLineEdit, 
                             QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QFrame, QStatusBar)
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class ClientSignals(QObject):
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

class ClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-RSA Client Enterprise")
        self.resize(600, 450)
        
        qdarktheme.setup_theme("dark", custom_colors={"primary": "#10b981"})
        
        self.signals = ClientSignals()
        self.signals.log_signal.connect(self.log)
        self.signals.status_signal.connect(self.update_status)
        
        self.socket = None
        self.session_key = os.urandom(16)
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 10)
        main_layout.setSpacing(15)
        
        # Header Panel
        header = QHBoxLayout()
        title_label = QLabel("💬 SECURE CHAT CONSOLE")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981;")
        header.addWidget(title_label)
        header.addStretch()
        
        self.connect_btn = QPushButton("Connect Securely")
        self.connect_btn.setMinimumWidth(150)
        self.connect_btn.setCursor(Qt.PointingHandCursor)
        self.connect_btn.clicked.connect(self.connect_server)
        header.addWidget(self.connect_btn)
        main_layout.addLayout(header)
        
        # Chat Area
        chat_frame = QFrame()
        chat_frame.setFrameShape(QFrame.StyledPanel)
        chat_frame.setStyleSheet("QFrame { border: 1px solid #334155; border-radius: 8px; }")
        frame_layout = QVBoxLayout(chat_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("font-family: Consolas, monospace; font-size: 14px; padding: 10px; border: none;")
        frame_layout.addWidget(self.chat_area)
        main_layout.addWidget(chat_frame)
        
        # Input Area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your encrypted message here...")
        self.input_field.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 6px;")
        self.input_field.returnPressed.connect(self.send_msg)
        self.send_btn = QPushButton("Send")
        self.send_btn.setMinimumWidth(80)
        self.send_btn.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 6px;")
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.clicked.connect(self.send_msg)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        main_layout.addLayout(input_layout)
        
        # Footer
        footer = QLabel("Sinh viên thực hiện: Trần Quốc Vũ - MSSV: 2380614820")
        footer.setStyleSheet("color: #64748b; font-style: italic; font-size: 12px;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)
        
        # Status
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("background-color: #0f172a; color: #94a3b8;")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Disconnected.")
        
        self.input_field.setEnabled(False)
        self.send_btn.setEnabled(False)
        
    def log(self, html_msg):
        if html_msg == "START_UI":
            self.input_field.setEnabled(True)
            self.send_btn.setEnabled(True)
            self.connect_btn.setText("✔ Connected")
            self.input_field.setFocus()
            self.update_status("Line secured via Hybrid AES-RSA")
        else:
            self.chat_area.append(html_msg)
            
    def update_status(self, msg):
        self.statusBar.showMessage(msg)
            
    def connect_server(self):
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Connecting...")
        self.update_status("Connecting to server...")
        threading.Thread(target=self.run_connection, daemon=True).start()
        
    def run_connection(self):
        host = '127.0.0.1'
        port = 12345
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            
            self.signals.log_signal.emit("<span style='color:#3b82f6'>[SYSTEM] Handshaking RSA public key...</span>")
            server_pub_bytes = self.socket.recv(2048)
            server_pub_key = serialization.load_pem_public_key(server_pub_bytes)
            
            enc_session_key = server_pub_key.encrypt(
                self.session_key,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            self.socket.send(enc_session_key)
            
            self.signals.log_signal.emit("<span style='color:#10b981'>✅ [SECURE LINE ESTABLISHED]</span> Ready to chat!")
            self.signals.log_signal.emit("START_UI")
            
        except Exception as e:
            self.signals.log_signal.emit(f"<span style='color:#ef4444'>❌ [ERROR] Connection Failed:</span> {e}")
            self.signals.status_signal.emit("Connection Error")
            # We would normally re-enable button via a signal, doing it raw here might be unsafe for PyQt 
            # but usually works for simple enabled state
            
    def send_msg(self):
        text = self.input_field.text().strip()
        if text and self.socket:
            self.chat_area.append(f"<span style='color:#34d399'><b>Me:</b></span> {text}")
            self.input_field.clear()
            
            try:
                cipher = AES.new(self.session_key, AES.MODE_CBC)
                iv = cipher.iv
                ciphertext = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
                self.socket.send(iv + ciphertext)
            except Exception as e:
                self.chat_area.append(f"<span style='color:#ef4444'>❌ Error: {e}</span>")

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
