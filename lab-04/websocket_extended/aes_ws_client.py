import tornado.ioloop
import tornado.websocket
import threading
import sys
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

AES_SECRET_KEY = b'HutechSecureKey!' 

def decrypt_aes(encrypted_base64: str) -> str:
    try:
        data = base64.b64decode(encrypted_base64)
        iv = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, iv=iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode('utf-8')
    except Exception as e:
        return f"[Chưa mã hoá / Thường là câu chào server]: {encrypted_base64}"

class AESWebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop

    def start(self):
        self.connect_and_read()

    def connect_and_read(self):
        print("Connecting to ws://localhost:8888/websocket/...")
        tornado.websocket.websocket_connect(
            url=f"ws://localhost:8888/websocket/",
            callback=self.on_connected,
            on_message_callback=self.on_message,
        )

    def on_connected(self, future):
        try:
            self.connection = future.result()
            print("Connected successfully! Mời bạn nhập thông điệp để máy chủ mã hoá...")
            threading.Thread(target=self.kb_input_thread, daemon=True).start()
        except Exception as e:
            print(f"Connection failed: {e}")
            self.io_loop.stop()

    def on_message(self, message):
        if message is None:
            print("Disconnected from server.")
            self.io_loop.stop()
            return

        print(f"\n[SERVER RAW CYPHERTEXT]: {message}")
        decrypted = decrypt_aes(message)
        print(f"[GIẢI MÃ DECRYPTED TEXT]: {decrypted}\n> ", end="", flush=True)

    def kb_input_thread(self):
        while True:
            try:
                # Need to use something simpler to not clash stdout with async 
                # but this is standard enough for demo
                msg = input()
                if msg.lower() == 'exit':
                    self.io_loop.add_callback(self.io_loop.stop)
                    break
                if self.connection:
                    self.connection.write_message(msg)
            except EOFError:
                break

def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = AESWebSocketClient(io_loop)
    io_loop.add_callback(client.start)
    try:
        io_loop.start()
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
