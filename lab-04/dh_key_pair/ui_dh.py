import sys
import qdarktheme
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QLabel, QGroupBox, QStatusBar, QFrame, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

global_parameters = None
alice_public_key = None
bob_public_key = None

class WorkerThread(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(object)

    def run(self):
        self.log_signal.emit("<span style='color:#fbbf24'>> Generating DH parameters (2048-bit). This might take a minute...</span>")
        parameters = dh.generate_parameters(generator=2, key_size=2048)
        self.log_signal.emit("<span style='color:#10b981'>> Parameters generated successfully!</span>")
        self.done_signal.emit(parameters)

class DHKeyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diffie-Hellman Key Exchange - Enterprise")
        self.resize(950, 750)
        
        # Setup modern dark theme from qdarktheme
        qdarktheme.setup_theme("dark", custom_colors={"primary": "#f59e0b"})

        self.alice_private = None
        self.bob_private = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 10)
        main_layout.setSpacing(15)

        title = QLabel("🔑 Diffie-Hellman Parameter Sync Center")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f59e0b; margin-bottom: 5px;")
        main_layout.addWidget(title)

        # Server Group
        setup_group = QGroupBox("Server Parameter Authority")
        setup_group.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; border-radius: 8px; margin-top: 15px; }")
        setup_layout = QVBoxLayout()
        setup_layout.setContentsMargins(15, 25, 15, 15)
        
        self.btn_gen_params = QPushButton("Generate Parameters & Keys")
        self.btn_gen_params.setMinimumHeight(45)
        self.btn_gen_params.setCursor(Qt.PointingHandCursor)
        self.btn_gen_params.clicked.connect(self.generate_params)
        setup_layout.addWidget(self.btn_gen_params)
        
        self.log_setup = QTextEdit()
        self.log_setup.setReadOnly(True)
        self.log_setup.setFixedHeight(120)
        self.log_setup.setStyleSheet("font-family: Consolas, monospace; font-size: 14px; background: #0f172a; border: 1px solid #334155; border-radius: 6px;")
        setup_layout.addWidget(self.log_setup)
        setup_group.setLayout(setup_layout)
        main_layout.addWidget(setup_group)

        # Alice & Bob Splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Alice Group
        alice_frame = QFrame()
        alice_layout = QVBoxLayout(alice_frame)
        alice_layout.setContentsMargins(0, 0, 5, 0)
        
        alice_group = QGroupBox("👩 Alice Client")
        alice_group.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #ec4899; }")
        al_vbox = QVBoxLayout()
        al_vbox.addWidget(QLabel("Public Key:"))
        self.txt_alice_pub = QTextEdit()
        self.txt_alice_pub.setReadOnly(True)
        self.txt_alice_pub.setStyleSheet("font-family: Consolas; font-size: 13px; color: #fbcfe8;")
        al_vbox.addWidget(self.txt_alice_pub)
        al_vbox.addWidget(QLabel("Shared Secret:"))
        self.txt_alice_shared = QTextEdit()
        self.txt_alice_shared.setReadOnly(True)
        self.txt_alice_shared.setFixedHeight(80)
        self.txt_alice_shared.setStyleSheet("font-family: Consolas; font-size: 14px; color: #bef264; font-weight: bold; border: 1px solid #10b981;")
        al_vbox.addWidget(self.txt_alice_shared)
        self.btn_alice_compute = QPushButton("Compute Shared Secret")
        self.btn_alice_compute.setMinimumHeight(40)
        self.btn_alice_compute.setCursor(Qt.PointingHandCursor)
        self.btn_alice_compute.setEnabled(False)
        self.btn_alice_compute.clicked.connect(self.alice_compute)
        al_vbox.addWidget(self.btn_alice_compute)
        alice_group.setLayout(al_vbox)
        alice_layout.addWidget(alice_group)
        splitter.addWidget(alice_frame)
        
        # Bob Group
        bob_frame = QFrame()
        bob_layout = QVBoxLayout(bob_frame)
        bob_layout.setContentsMargins(5, 0, 0, 0)
        
        bob_group = QGroupBox("👨 Bob Client")
        bob_group.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #3b82f6; }")
        bo_vbox = QVBoxLayout()
        bo_vbox.addWidget(QLabel("Public Key:"))
        self.txt_bob_pub = QTextEdit()
        self.txt_bob_pub.setReadOnly(True)
        self.txt_bob_pub.setStyleSheet("font-family: Consolas; font-size: 13px; color: #bfdbfe;")
        bo_vbox.addWidget(self.txt_bob_pub)
        bo_vbox.addWidget(QLabel("Shared Secret:"))
        self.txt_bob_shared = QTextEdit()
        self.txt_bob_shared.setReadOnly(True)
        self.txt_bob_shared.setFixedHeight(80)
        self.txt_bob_shared.setStyleSheet("font-family: Consolas; font-size: 14px; color: #bef264; font-weight: bold; border: 1px solid #10b981;")
        bo_vbox.addWidget(self.txt_bob_shared)
        self.btn_bob_compute = QPushButton("Compute Shared Secret")
        self.btn_bob_compute.setMinimumHeight(40)
        self.btn_bob_compute.setCursor(Qt.PointingHandCursor)
        self.btn_bob_compute.setEnabled(False)
        self.btn_bob_compute.clicked.connect(self.bob_compute)
        bo_vbox.addWidget(self.btn_bob_compute)
        bob_group.setLayout(bo_vbox)
        bob_layout.addWidget(bob_group)
        splitter.addWidget(bob_frame)
        
        main_layout.addWidget(splitter)

        # Footer
        footer = QLabel("Sinh viên thực hiện: Trần Quốc Vũ - MSSV: 2380614820")
        footer.setStyleSheet("color: #64748b; font-style: italic; font-size: 12px;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)
        
        # StatusBar
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("background-color: #0f172a; color: #94a3b8;")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Idle - Waiting for parameter generation.")

    def generate_params(self):
        self.btn_gen_params.setEnabled(False)
        self.log_setup.clear()
        self.statusBar.showMessage("Generating P & G parameters...")
        
        self.worker = WorkerThread()
        self.worker.log_signal.connect(self.log_setup.append)
        self.worker.done_signal.connect(self.on_params_generated)
        self.worker.start()

    def on_params_generated(self, parameters):
        global global_parameters, alice_public_key, bob_public_key
        global_parameters = parameters
        
        self.log_setup.append("<span style='color:#60a5fa'>> Generating Key Pairs for Alice and Bob...</span>")
        
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

        self.log_setup.append("<span style='color:#10b981'>> Key pairs distributed successfully. Waiting for clients to compute shared secret.</span>")
        self.statusBar.showMessage("Parameter setup complete. Clients can now compute Shared Secret.")
        self.btn_alice_compute.setEnabled(True)
        self.btn_bob_compute.setEnabled(True)

    def alice_compute(self):
        global bob_public_key
        if bob_public_key and self.alice_private:
            shared_key = self.alice_private.exchange(bob_public_key)
            self.txt_alice_shared.setPlainText(shared_key.hex())
            self.btn_alice_compute.setEnabled(False)
            self.statusBar.showMessage("Alice computed shared secret successfully.")

    def bob_compute(self):
        global alice_public_key
        if alice_public_key and self.bob_private:
            shared_key = self.bob_private.exchange(alice_public_key)
            self.txt_bob_shared.setPlainText(shared_key.hex())
            self.btn_bob_compute.setEnabled(False)
            self.statusBar.showMessage("Bob computed shared secret successfully.")

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = DHKeyApp()
    window.show()
    sys.exit(app.exec_())
