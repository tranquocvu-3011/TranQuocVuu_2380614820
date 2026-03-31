import sys
import socket
import threading
import qdarktheme
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QLabel, QStatusBar, QFrame)
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class ServerSignals(QObject):
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

class ServerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-RSA Server Enterprise")
        self.resize(700, 500)
        
        # Setup modern dark theme from qdarktheme
        qdarktheme.setup_theme("dark", custom_colors={"primary": "#3b82f6"})
        
        self.signals = ServerSignals()
        self.signals.log_signal.connect(self.log)
        self.signals.status_signal.connect(self.update_status)
        
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
        self.session_key = None
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 10)
        main_layout.setSpacing(15)
        
        # Header Panel
        header = QHBoxLayout()
        title_label = QLabel("🚀 SERVER EVENT LOG")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #3b82f6;")
        header.addWidget(title_label)
        header.addStretch()
        
        self.start_btn = QPushButton("Start Server")
        self.start_btn.setMinimumWidth(150)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.clicked.connect(self.start_server)
        header.addWidget(self.start_btn)
        main_layout.addLayout(header)
        
        # Log Area inside a Frame
        log_frame = QFrame()
        log_frame.setFrameShape(QFrame.StyledPanel)
        log_frame.setStyleSheet("QFrame { border: 1px solid #334155; border-radius: 8px; }")
        frame_layout = QVBoxLayout(log_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("font-family: Consolas, monospace; font-size: 14px; padding: 10px; border: none;")
        frame_layout.addWidget(self.log_area)
        main_layout.addWidget(log_frame)
        
        # Footer
        footer = QLabel("Sinh viên thực hiện: Trần Quốc Vũ - MSSV: 2380614820")
        footer.setStyleSheet("color: #64748b; font-style: italic; font-size: 12px;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)
        
        # Status Bar
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("background-color: #0f172a; color: #94a3b8;")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Idle - Ready to start.")
        
    def log(self, html_msg):
        self.log_area.append(html_msg)
        
    def update_status(self, msg):
        self.statusBar.showMessage(msg)
        
    def start_server(self):
        self.start_btn.setEnabled(False)
        self.start_btn.setText("● Server is Running")
        self.update_status("Starting socket listener...")
        threading.Thread(target=self.run_socket, daemon=True).start()
        
    def run_socket(self):
        host = '127.0.0.1'
        port = 12345
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(5)
            self.signals.log_signal.emit(f"<span style='color:#10b981'>✅ [SYSTEM]</span> Server listening on port {port}...")
            self.signals.status_signal.emit(f"Listening on {host}:{port}")
            
            while True:
                client_socket, addr = server_socket.accept()
                self.signals.log_signal.emit(f"<span style='color:#3b82f6'>🔗 [CONNECT]</span> Accepted connection from {addr}")
                threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
        except Exception as e:
            self.signals.log_signal.emit(f"<span style='color:#ef4444'>❌ [ERROR]</span> {e}")
            
    def handle_client(self, client_socket, addr):
        try:
            pub_bytes = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            client_socket.send(pub_bytes)
            
            enc_session_key = client_socket.recv(2048)
            self.session_key = self.private_key.decrypt(
                enc_session_key,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            self.signals.log_signal.emit(f"<span style='color:#f59e0b'>🔑 [CRYPTO]</span> Decrypted AES Session Key from {addr}")
            
            while True:
                data = client_socket.recv(4096)
                if not data: break
                try:
                    iv = data[:16]
                    ciphertext = data[16:]
                    cipher = AES.new(self.session_key, AES.MODE_CBC, iv=iv)
                    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
                    
                    self.signals.log_signal.emit(f"<span style='color:#a7f3d0'>[{addr[1]}]:</span> <b>{plaintext.decode('utf-8')}</b>")
                except Exception as e:
                    self.signals.log_signal.emit(f"<span style='color:#ef4444'>❌ [ERROR]</span> Decrypt Failed: {e}")
        except Exception as e:
            self.signals.log_signal.emit(f"<span style='color:#94a3b8'>🔌 [DISCONNECT]</span> {addr} has left.")
        finally:
            client_socket.close()

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = ServerApp()
    window.show()
    sys.exit(app.exec_())
