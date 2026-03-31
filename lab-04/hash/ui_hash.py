import sys
import hashlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import Qt
from Crypto.Hash import SHA3_256

class HashApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hash Calculator")
        self.resize(600, 450)
        self.setStyleSheet("""
            QWidget { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                font-size: 13px; 
                background-color: #f7f9fc;
                color: #1e293b; 
            }
            QComboBox {
                padding: 6px;
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                background-color: white;
                font-weight: bold;
                color: #0f172a;
            }
            QTextEdit { 
                background: white; 
                border: 1px solid #cbd5e1; 
                border-radius: 4px; 
                padding: 10px; 
                color: #1e293b; 
            }
            QTextEdit:focus { border: 1px solid #3b82f6; }
            QPushButton { 
                background-color: #10b981; 
                color: white; 
                border: none; 
                border-radius: 4px; 
                padding: 12px; 
                font-weight: bold; 
                font-size: 14px; 
            }
            QPushButton:hover { background-color: #059669; }
            QLabel.footer { color: #64748b; font-size: 12px; margin-top: 5px; }
            QLabel.title { font-size: 16px; font-weight: bold; color: #0f172a; margin-bottom: 5px; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Hash Generator")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("Select Algorithm:"))
        self.algo_box = QComboBox()
        self.algo_box.addItems(["MD5 (Manual Simulation)", "MD5 (Library)", "SHA-256", "SHA-3 (PyCryptodome)", "BLAKE2"])
        self.algo_box.setCursor(Qt.PointingHandCursor)
        combo_layout.addWidget(self.algo_box)
        layout.addLayout(combo_layout)

        layout.addWidget(QLabel("Input Text:"))
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text to hash...")
        self.input_text.setFixedHeight(80)
        layout.addWidget(self.input_text)
        
        self.btn_hash = QPushButton("Generate Hash")
        self.btn_hash.setCursor(Qt.PointingHandCursor)
        self.btn_hash.clicked.connect(self.compute_hash)
        layout.addWidget(self.btn_hash)

        layout.addWidget(QLabel("Hash Output (Hex):"))
        self.output_hash = QTextEdit()
        self.output_hash.setReadOnly(True)
        self.output_hash.setStyleSheet("font-family: Consolas, monospace; font-size: 14px; color: #dc2626;")
        self.output_hash.setFixedHeight(80)
        layout.addWidget(self.output_hash)
        
        footer = QLabel("Sinh viên thực hiện: Trần Quốc Vũ - MSSV: 2380614820")
        footer.setProperty("class", "footer")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

    def compute_hash(self):
        text = self.input_text.toPlainText().encode('utf-8')
        algo_idx = self.algo_box.currentIndex()
        
        try:
            if algo_idx == 0:
                res = hashlib.md5(text).hexdigest()
            elif algo_idx == 1:
                res = hashlib.md5(text).hexdigest()
            elif algo_idx == 2:
                res = hashlib.sha256(text).hexdigest()
            elif algo_idx == 3:
                h = SHA3_256.new()
                h.update(text)
                res = h.hexdigest()
            elif algo_idx == 4:
                res = hashlib.blake2b(text).hexdigest()
            
            self.output_hash.setPlainText(res)
        except Exception as e:
            self.output_hash.setPlainText(f"Error: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HashApp()
    window.show()
    sys.exit(app.exec_())
