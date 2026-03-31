import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class ClientSignals(QObject):
    log_msg = pyqtSignal(str)

class ClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-RSA Socket Client")
        self.setGeometry(650, 100, 500, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.layout.addWidget(self.log_area)
        
        self.input_layout = QHBoxLayout()
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Enter message ('exit' to quit)...")
        self.msg_input.returnPressed.connect(self.send_msg)
        self.btn_send = QPushButton("Send")
        self.btn_send.clicked.connect(self.send_msg)
        self.btn_connect = QPushButton("Connect to Server")
        self.btn_connect.clicked.connect(self.connect_server)
        
        self.input_layout.addWidget(self.msg_input)
        self.input_layout.addWidget(self.btn_send)
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.btn_connect)
        
        self.signals = ClientSignals()
        self.signals.log_msg.connect(self.append_log)
        
        self.client_socket = None
        self.aes_key = None
        self.is_connected = False

    def append_log(self, msg):
        self.log_area.append(msg)

    def encrypt_message(self, key, message):
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ciphertext

    def decrypt_message(self, key, encrypted_message):
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_message.decode()

    def receive_loop(self):
        while self.is_connected:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if not encrypted_message:
                    break
                decrypted_message = self.decrypt_message(self.aes_key, encrypted_message)
                self.signals.log_msg.emit(f"Received: {decrypted_message}")
            except Exception as e:
                self.signals.log_msg.emit("Connection lost or closed.")
                break
        self.is_connected = False
        self.btn_connect.setEnabled(True)

    def connect_server(self):
        if self.is_connected:
            return
        
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 12345))
            
            # Generate RSA key pair for client
            client_key = RSA.generate(2048)
            
            # Receive server's public key
            server_public_key = RSA.import_key(self.client_socket.recv(2048))
            
            # Send client's public key
            self.client_socket.send(client_key.publickey().export_key(format='PEM'))
            
            # Receive AES encrypted key
            encrypted_aes_key = self.client_socket.recv(2048)
            cipher_rsa = PKCS1_OAEP.new(client_key)
            self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)
            
            self.is_connected = True
            self.btn_connect.setEnabled(False)
            self.signals.log_msg.emit("Connected to Server securely via AES-RSA Hybrid Exchange!")
            
            receive_thread = threading.Thread(target=self.receive_loop)
            receive_thread.daemon = True
            receive_thread.start()
        except Exception as e:
            self.signals.log_msg.emit(f"Connection failed: {e}")

    def send_msg(self):
        if not self.is_connected:
            self.signals.log_msg.emit("Not connected!")
            return
            
        msg = self.msg_input.text()
        if msg:
            try:
                self.signals.log_msg.emit(f"Me: {msg}")
                self.client_socket.send(self.encrypt_message(self.aes_key, msg))
                self.msg_input.clear()
            except Exception as e:
                self.signals.log_msg.emit(f"Send failed: {e}")
                
    def closeEvent(self, event):
        if self.is_connected:
            try:
                self.client_socket.send(self.encrypt_message(self.aes_key, "exit"))
                self.client_socket.close()
            except:
                pass
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
