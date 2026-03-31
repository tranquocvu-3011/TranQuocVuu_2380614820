import tornado.ioloop
import tornado.web
import tornado.websocket
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Use a static key for demonstration (16 bytes for AES-128)
AES_SECRET_KEY = b'HutechSecureKey!' 

def encrypt_aes(message: str) -> str:
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    # Return Base64 encoded payload: IV + Ciphertext
    return base64.b64encode(iv + ciphertext).decode('utf-8')

class AESWebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)
        print(f"New client connected. Total clients: {len(self.clients)}")
        self.write_message("Welcome! Send me a message and I will AES encrypt it.")

    def on_close(self):
        self.clients.remove(self)
        print("Client disconnected.")

    def on_message(self, message):
        print(f"Received plain message from client: {message}")
        encrypted_response = encrypt_aes(message)
        print(f"Sending encrypted message: {encrypted_response}")
        self.write_message(encrypted_response)

def main():
    app = tornado.web.Application(
        [(r"/websocket/", AESWebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )
    app.listen(8888)
    print("AES WebSocket Server started on ws://localhost:8888/websocket/")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
