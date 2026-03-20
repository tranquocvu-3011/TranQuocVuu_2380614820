import os
import sys
from string import ascii_uppercase

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from ui.caesar import Ui_MainWindow

ALPHABET = list(ascii_uppercase)


def encrypt_text(text: str, key: int) -> str:
    alphabet_len = len(ALPHABET)
    text = text.upper()
    encrypted_text = []
    for letter in text:
        if letter in ALPHABET:
            letter_index = ALPHABET.index(letter)
            output_index = (letter_index + key) % alphabet_len
            encrypted_text.append(ALPHABET[output_index])
        else:
            encrypted_text.append(letter)
    return "".join(encrypted_text)


def decrypt_text(text: str, key: int) -> str:
    alphabet_len = len(ALPHABET)
    text = text.upper()
    decrypted_text = []
    for letter in text:
        if letter in ALPHABET:
            letter_index = ALPHABET.index(letter)
            output_index = (letter_index - key) % alphabet_len
            decrypted_text.append(ALPHABET[output_index])
        else:
            decrypted_text.append(letter)
    return "".join(decrypted_text)


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect buttons
        self.ui.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.handle_decrypt)

    def get_key(self):
        """Lấy và kiểm tra key nhập vào."""
        key_str = self.ui.txt_key.text().strip()
        if not key_str:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Key (số nguyên)!")
            return None
        try:
            return int(key_str)
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Key phải là số nguyên!")
            return None

    def handle_encrypt(self):
        plain = self.ui.txt_plain_text.toPlainText().strip()
        if not plain:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Plain Text!")
            return
        key = self.get_key()
        if key is None:
            return
        result = encrypt_text(plain, key)
        self.ui.txt_cipher_text.setPlainText(result)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Thành công")
        msg.setText("Encrypted Successfully!")
        msg.exec_()

    def handle_decrypt(self):
        cipher = self.ui.txt_cipher_text.toPlainText().strip()
        if not cipher:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập CipherText!")
            return
        key = self.get_key()
        if key is None:
            return
        result = decrypt_text(cipher, key)
        self.ui.txt_plain_text.setPlainText(result)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Thành công")
        msg.setText("Decrypted Successfully!")
        msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
