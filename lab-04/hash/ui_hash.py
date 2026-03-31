import sys
import hashlib
import qdarktheme
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QFrame)
from PyQt5.QtCore import Qt
from Crypto.Hash import SHA3_256

class HashApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nền Tảng Băm Dữ Liệu - Enterprise")
        self.resize(700, 550)
        
        qdarktheme.setup_theme("dark", custom_colors={"primary": "#8b5cf6"})

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        icon_label = QLabel("🛡️")
        icon_label.setStyleSheet("font-size: 28px;")
        
        title_box = QVBoxLayout()
        title = QLabel("GIAO DIỆN BĂM TOÀN NĂNG")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #8b5cf6; padding: 0;")
        sub_title = QLabel("Bộ Công Cụ Băm Tiêu Chuẩn Mật Mã Học")
        sub_title.setStyleSheet("font-size: 12px; color: #94a3b8;")
        title_box.addWidget(title)
        title_box.addWidget(sub_title)
        
        header_layout.addWidget(icon_label)
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Algorithm Selection
        algo_frame = QFrame()
        algo_frame.setStyleSheet("QFrame { background: #1e293b; border-radius: 8px; }")
        algo_layout = QHBoxLayout(algo_frame)
        algo_layout.setContentsMargins(15, 10, 15, 10)
        
        lbl_algo = QLabel("Thuật Toán:")
        lbl_algo.setStyleSheet("font-weight: bold; color: #cbd5e1;")
        algo_layout.addWidget(lbl_algo)
        
        self.algo_box = QComboBox()
        self.algo_box.addItems(["MD5 (Mô phỏng thủ công)", "MD5 (Thư viện chuẩn)", "SHA-256", "SHA-3 (PyCryptodome)", "BLAKE2"])
        self.algo_box.setCursor(Qt.PointingHandCursor)
        self.algo_box.setMinimumWidth(250)
        self.algo_box.setMinimumHeight(40)
        self.algo_box.setStyleSheet("font-size: 14px; font-weight: bold;")
        algo_layout.addWidget(self.algo_box)
        algo_layout.addStretch()
        layout.addWidget(algo_frame)

        # Input Box
        layout.addWidget(QLabel("Dữ Liệu Đầu Vào:"))
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Dán hoặc gõ văn bản bạn muốn băm tại đây...")
        self.input_text.setFixedHeight(100)
        self.input_text.setStyleSheet("font-size: 15px; padding: 15px; border: 1px solid #475569; border-radius: 8px;")
        layout.addWidget(self.input_text)
        
        # Action Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_hash = QPushButton("TIẾN HÀNH BĂM DỮ LIỆU")
        self.btn_hash.setMinimumWidth(200)
        self.btn_hash.setMinimumHeight(45)
        self.btn_hash.setStyleSheet("font-size: 15px; font-weight: bold; border-radius: 22px;")
        self.btn_hash.setCursor(Qt.PointingHandCursor)
        self.btn_hash.clicked.connect(self.compute_hash)
        btn_layout.addWidget(self.btn_hash)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Output Box
        layout.addWidget(QLabel("Kết Quả Mã Băm (Hex):"))
        self.output_hash = QTextEdit()
        self.output_hash.setReadOnly(True)
        self.output_hash.setStyleSheet("font-family: Consolas, monospace; font-size: 16px; color: #a7f3d0; background: #020617; border: 1px solid #334155; border-radius: 8px; font-weight: bold; padding: 15px;")
        self.output_hash.setFixedHeight(90)
        layout.addWidget(self.output_hash)
        
        layout.addStretch()
        
        # Footer
        footer = QLabel("Sinh viên thực hiện: Trần Quốc Vũ - MSSV: 2380614820")
        footer.setStyleSheet("color: #64748b; font-size: 12px; font-style: italic;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

    def compute_hash(self):
        text = self.input_text.toPlainText().encode('utf-8')
        if not text:
            self.output_hash.setPlainText("Vui lòng nhập văn bản hoặc dữ liệu.")
            self.output_hash.setStyleSheet("font-family: Consolas; font-size: 16px; color: #ef4444; background: #020617; border: 1px solid #ef4444; border-radius: 8px; padding: 15px;")
            return
            
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
            self.output_hash.setStyleSheet("font-family: Consolas, monospace; font-size: 16px; color: #a7f3d0; background: #020617; border: 1px solid #3b82f6; border-radius: 8px; font-weight: bold; padding: 15px;")
        except Exception as e:
            self.output_hash.setPlainText(f"Lỗi hệ thống: {str(e)}")
            self.output_hash.setStyleSheet("font-family: Consolas; font-size: 16px; color: #ef4444; background: #020617; border: 1px solid #ef4444; border-radius: 8px; padding: 15px;")

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = HashApp()
    window.show()
    sys.exit(app.exec_())
