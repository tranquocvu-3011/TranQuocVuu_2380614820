import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QGroupBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

# Global params to simulate network
global_parameters = None
alice_public_key = None
bob_public_key = None

class WorkerThread(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(object)

    def run(self):
        self.log_signal.emit("> Generating DH parameters (2048-bit). This might take a minute...")
        parameters = dh.generate_parameters(generator=2, key_size=2048)
        self.log_signal.emit("> Parameters generated successfully!")
        self.done_signal.emit(parameters)

class DHKeyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bộ Sinh Khóa Diffie-Hellman (Bản Độc Quyền)")
        self.resize(1100, 850)
        self.setStyleSheet("""
            QWidget { 
                font-family: 'Segoe UI', Inter, sans-serif; 
                font-size: 14px; 
                background-color: #0f172a; 
                color: #e2e8f0; 
            }
            QGroupBox { 
                border: 2px solid #334155; 
                border-radius: 8px; 
                margin-top: 15px; 
                padding: 15px; 
                font-weight: bold; 
                color: #38bdf8; 
                font-size: 15px;
            }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }
            QTextEdit { 
                background: #1e293b; 
                border: 1px solid #475569; 
                border-radius: 6px; 
                padding: 12px; 
                color: #a7f3d0; 
                font-family: Consolas, monospace;
            }
            QPushButton { 
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #3b82f6, stop: 1 #2563eb); 
                color: white; 
                border: none; 
                border-radius: 6px; 
                padding: 12px; 
                font-weight: bold; 
                font-size: 15px; 
            }
            QPushButton:hover { background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #60a5fa, stop: 1 #3b82f6); }
            QPushButton:disabled { background-color: #334155; color: #94a3b8; }
            QLabel.footer { color: #94a3b8; font-style: italic; font-weight: bold; font-size: 14px; margin-top: 5px; }
        """)

        # Components
        self.alice_private = None
        self.bob_private = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. SETUP GROUP
        setup_group = QGroupBox("🌐 TRUNG TÂM PHÁT MÃ (SERVER PARAMS)")
        setup_layout = QVBoxLayout()
        self.btn_gen_params = QPushButton("🔥 KÍCH HOẠT THAM SỐ VÀ CẤP PHÁT KHÓA")
        self.btn_gen_params.setCursor(Qt.PointingHandCursor)
        self.btn_gen_params.clicked.connect(self.generate_params)
        self.log_setup = QTextEdit()
        self.log_setup.setReadOnly(True)
        self.log_setup.setFixedHeight(120)
        setup_layout.addWidget(self.btn_gen_params)
        setup_layout.addWidget(self.log_setup)
        setup_group.setLayout(setup_layout)
        main_layout.addWidget(setup_group)

        # BOTTOM LAYOUT
        bottom_layout = QHBoxLayout()
        
        # 2. ALICE
        alice_group = QGroupBox("👩 ALICE CLIENT")
        alice_layout = QVBoxLayout()
        alice_layout.addWidget(QLabel("Mã Công Khai (Public Key):"))
        self.txt_alice_pub = QTextEdit()
        self.txt_alice_pub.setReadOnly(True)
        alice_layout.addWidget(self.txt_alice_pub)
        alice_layout.addWidget(QLabel("Mã Bí Mật Chung (Shared Secret):"))
        self.txt_alice_shared = QTextEdit()
        self.txt_alice_shared.setStyleSheet("color: #fca5a5;")
        self.txt_alice_shared.setReadOnly(True)
        self.txt_alice_shared.setFixedHeight(100)
        alice_layout.addWidget(self.txt_alice_shared)
        self.btn_alice_compute = QPushButton("💻 TÍNH TOÁN SHARED SECRET")
        self.btn_alice_compute.setCursor(Qt.PointingHandCursor)
        self.btn_alice_compute.setEnabled(False)
        self.btn_alice_compute.clicked.connect(self.alice_compute)
        alice_layout.addWidget(self.btn_alice_compute)
        alice_group.setLayout(alice_layout)
        
        # 3. BOB
        bob_group = QGroupBox("👨 BOB CLIENT")
        bob_layout = QVBoxLayout()
        bob_layout.addWidget(QLabel("Mã Công Khai (Public Key):"))
        self.txt_bob_pub = QTextEdit()
        self.txt_bob_pub.setReadOnly(True)
        bob_layout.addWidget(self.txt_bob_pub)
        bob_layout.addWidget(QLabel("Mã Bí Mật Chung (Shared Secret):"))
        self.txt_bob_shared = QTextEdit()
        self.txt_bob_shared.setStyleSheet("color: #fca5a5;")
        self.txt_bob_shared.setReadOnly(True)
        self.txt_bob_shared.setFixedHeight(100)
        bob_layout.addWidget(self.txt_bob_shared)
        self.btn_bob_compute = QPushButton("💻 TÍNH TOÁN SHARED SECRET")
        self.btn_bob_compute.setCursor(Qt.PointingHandCursor)
        self.btn_bob_compute.setEnabled(False)
        self.btn_bob_compute.clicked.connect(self.bob_compute)
        bob_layout.addWidget(self.btn_bob_compute)
        bob_group.setLayout(bob_layout)
        
        bottom_layout.addWidget(alice_group)
        bottom_layout.addWidget(bob_group)
        main_layout.addLayout(bottom_layout)

        # FOOTER
        footer = QLabel("🚀 Đồ án Mật mã học - Sinh viên thực hiện: Trần Quốc Vũ (2380614820)")
        footer.setProperty("class", "footer")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

    def generate_params(self):
        self.btn_gen_params.setEnabled(False)
        self.log_setup.clear()
        
        self.worker = WorkerThread()
        self.worker.log_signal.connect(self.log_setup.append)
        self.worker.done_signal.connect(self.on_params_generated)
        self.worker.start()

    def on_params_generated(self, parameters):
        global global_parameters, alice_public_key, bob_public_key
        global_parameters = parameters
        
        self.log_setup.append("> Generating Key Pairs for Alice and Bob...")
        
        self.alice_private = parameters.generate_private_key()
        alice_public_key = self.alice_private.public_key()
        
        self.bob_private = parameters.generate_private_key()
        bob_public_key = self.bob_private.public_key()
        
        self.txt_alice_pub.setPlainText(alice_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode())
        
        self.txt_bob_pub.setPlainText(bob_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode())

        self.log_setup.append("> Đã phát tán Public Keys cho Alice và Bob thành công.")
        self.btn_alice_compute.setEnabled(True)
        self.btn_bob_compute.setEnabled(True)

    def alice_compute(self):
        global bob_public_key
        if bob_public_key and self.alice_private:
            shared_key = self.alice_private.exchange(bob_public_key)
            self.txt_alice_shared.setPlainText(shared_key.hex())
            self.log_setup.append("> Alice đã tính toán thành công Shared Secret!")
            self.btn_alice_compute.setEnabled(False)

    def bob_compute(self):
        global alice_public_key
        if alice_public_key and self.bob_private:
            shared_key = self.bob_private.exchange(alice_public_key)
            self.txt_bob_shared.setPlainText(shared_key.hex())
            self.log_setup.append("> Bob đã tính toán thành công Shared Secret!")
            self.btn_bob_compute.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DHKeyApp()
    window.show()
    sys.exit(app.exec_())
