import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QFont
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class ServerSignals(QObject):
    log_signal = pyqtSignal(str)

class ServerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-RSA Socket Server (Bản Cao Cấp)")
        self.resize(700, 500)
        self.setStyleSheet("""
            QWidget { 
                font-family: 'Segoe UI', Inter, Arial, sans-serif; 
                font-size: 14px; 
                background-color: #0f172a; /* Dark Blue Slate */
                color: #f8fafc; 
            }
            QTextEdit { 
                background: #1e293b; 
                border: 1px solid #334155; 
                border-radius: 8px; 
                padding: 12px; 
                color: #38bdf8; /* Light blue text for sci-fi feel */
                font-size: 14px;
                font-family: Consolas, monospace;
            }
            QTextEdit:focus { border: 2px solid #3b82f6; }
            QPushButton { 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #3b82f6, stop: 1 #2563eb); 
                color: white; 
                border: none; 
                border-radius: 6px; 
                padding: 12px; 
                font-weight: bold; 
                font-size: 15px; 
            }
            QPushButton:hover { 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #60a5fa, stop: 1 #3b82f6); 
            }
            QPushButton:disabled { background-color: #475569; color: #94a3b8; }
            QLabel.footer { color: #94a3b8; font-style: italic; font-weight: bold; font-size: 13px; margin-top: 5px; }
            QLabel.title { font-size: 18px; font-weight: bold; color: #60a5fa; margin-bottom: 5px; }
        """)
        
        self.signals = ServerSignals()
        self.signals.log_signal.connect(self.log)
        
        # RSA Keys
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
        self.session_key = None
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(25, 25, 25, 20)
        layout.setSpacing(15)
        
        lb_title = QLabel("🛡️ SERVER ĐIỀU KHIỂN SỰ KIỆN (EVENT LOG):")
        lb_title.setProperty("class", "title")
        layout.addWidget(lb_title)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        
        self.start_btn = QPushButton("🚀 KÍCH HOẠT LẮNG NGHE (START SERVER)")
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.clicked.connect(self.start_server)
        layout.addWidget(self.start_btn)
        
        footer = QLabel("👨‍💻 Sinh viên thực hiện: Trần Quốc Vũ - Đồ án Lab 4")
        footer.setProperty("class", "footer")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
    def log(self, message):
        self.log_area.append(message)
        
    def start_server(self):
        self.start_btn.setEnabled(False)
        self.start_btn.setText("📡 HỆ THỐNG ĐANG LẮNG NGHE (RUNNING)")
        threading.Thread(target=self.run_socket, daemon=True).start()
        
    def run_socket(self):
        host = '127.0.0.1'
        port = 12345
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        self.signals.log_signal.emit(f"✅ HỆ THỐNG SẴN SÀNG TẠI PORT {port}...")
        
        while True:
            client_socket, addr = server_socket.accept()
            self.signals.log_signal.emit(f"\n🔌 THIẾT BỊ MỚI TRUY CẬP: {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
            
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
            self.signals.log_signal.emit(f"🔑 ĐÃ NHẬN KHÓA BÍ MẬT AES TỪ {addr}")
            
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    iv = data[:16]
                    ciphertext = data[16:]
                    cipher = AES.new(self.session_key, AES.MODE_CBC, iv=iv)
                    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
                    self.signals.log_signal.emit(f"[{addr[1]}]: {plaintext.decode('utf-8')}")
                except Exception as e:
                    self.signals.log_signal.emit(f"❌ Lỗi giải mã: {e}")
                    
        except Exception as e:
            self.signals.log_signal.emit(f"❌ Đứt kết nối với {addr}: {e}")
        finally:
            client_socket.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServerApp()
    window.show()
    sys.exit(app.exec_())
