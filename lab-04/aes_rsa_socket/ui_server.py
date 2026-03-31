import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, QObject
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class ServerSignals(QObject):
    log_msg = pyqtSignal(str)

class ServerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-RSA Socket Server")
        self.setGeometry(100, 100, 500, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel("Server Event Log:")
        self.layout.addWidget(self.label)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.layout.addWidget(self.log_area)
        
        self.btn_start = QPushButton("Start Server")
        self.btn_start.clicked.connect(self.start_server)
        self.layout.addWidget(self.btn_start)
        
        self.signals = ServerSignals()
        self.signals.log_msg.connect(self.append_log)
        
        self.server_socket = None
        self.server_key = RSA.generate(2048)
        self.clients = []
        self.is_running = False

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

    def handle_client(self, client_socket, client_address):
        self.signals.log_msg.emit(f"Connected with {client_address}")
        try:
            client_socket.send(self.server_key.publickey().export_key(format='PEM'))
            client_received_key = RSA.import_key(client_socket.recv(2048))
            
            aes_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(client_received_key)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            client_socket.send(encrypted_aes_key)
            
            self.clients.append((client_socket, aes_key))
            
            while self.is_running:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break
                decrypted_message = self.decrypt_message(aes_key, encrypted_message)
                self.signals.log_msg.emit(f"[{client_address[1]}]: {decrypted_message}")
                
                # Broadcaster
                for client, key in self.clients:
                    if client != client_socket:
                        encrypted = self.encrypt_message(key, decrypted_message)
                        client.send(encrypted)
                
                if decrypted_message == "exit":
                    break
        except Exception as e:
            self.signals.log_msg.emit(f"Error {client_address}: {e}")
            
        if (client_socket, aes_key) in self.clients:
            self.clients.remove((client_socket, aes_key))
        client_socket.close()
        self.signals.log_msg.emit(f"Connection with {client_address} closed")

    def server_loop(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(5)
        self.signals.log_msg.emit("Server is waiting for connections on port 12345...")
        
        while self.is_running:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
            except Exception:
                break

    def start_server(self):
        if not self.is_running:
            self.is_running = True
            self.btn_start.setEnabled(False)
            self.server_thread = threading.Thread(target=self.server_loop)
            self.server_thread.daemon = True
            self.server_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerApp()
    window.show()
    sys.exit(app.exec_())
