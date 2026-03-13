from flask import Flask, render_template, request

from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()
transposition_cipher = TranspositionCipher()

CIPHERS = {
    "caesar": "Caesar",
    "vigenere": "Vigenere",
    "railfence": "Rail Fence",
    "playfair": "Playfair",
    "transposition": "Transposition",
}


@app.route("/")
def index():
    return render_template("index.html", ciphers=CIPHERS)


@app.route("/<cipher_name>", methods=["GET", "POST"])
def cipher_page(cipher_name):
    if cipher_name not in CIPHERS:
        return "Cipher not found", 404

    context = {
        "cipher_name": cipher_name,
        "cipher_label": CIPHERS[cipher_name],
        "plain_text": "",
        "cipher_text": "",
        "key": "",
        "result": "",
        "matrix": None,
        "error": "",
    }

    if request.method == "POST":
        context["plain_text"] = request.form.get("plain_text", "")
        context["cipher_text"] = request.form.get("cipher_text", "")
        context["key"] = request.form.get("key", "")
        action = request.form.get("action", "")

        try:
            key = context["key"]

            if cipher_name == "caesar":
                key_int = int(key)
                if action == "encrypt":
                    context["result"] = caesar_cipher.encrypt_text(context["plain_text"], key_int)
                elif action == "decrypt":
                    context["result"] = caesar_cipher.decrypt_text(context["cipher_text"], key_int)

            elif cipher_name == "vigenere":
                if action == "encrypt":
                    context["result"] = vigenere_cipher.vigenere_encrypt(context["plain_text"], key)
                elif action == "decrypt":
                    context["result"] = vigenere_cipher.vigenere_decrypt(context["cipher_text"], key)

            elif cipher_name == "railfence":
                key_int = int(key)
                if action == "encrypt":
                    context["result"] = railfence_cipher.rail_fence_encrypt(context["plain_text"], key_int)
                elif action == "decrypt":
                    context["result"] = railfence_cipher.rail_fence_decrypt(context["cipher_text"], key_int)

            elif cipher_name == "playfair":
                matrix = playfair_cipher.create_playfair_matrix(key)
                context["matrix"] = matrix
                if action == "create_matrix":
                    context["result"] = "Matrix created"
                elif action == "encrypt":
                    context["result"] = playfair_cipher.playfair_encrypt(context["plain_text"], matrix)
                elif action == "decrypt":
                    context["result"] = playfair_cipher.playfair_decrypt(context["cipher_text"], matrix)

            elif cipher_name == "transposition":
                key_int = int(key)
                if action == "encrypt":
                    context["result"] = transposition_cipher.encrypt(context["plain_text"], key_int)
                elif action == "decrypt":
                    context["result"] = transposition_cipher.decrypt(context["cipher_text"], key_int)

            if action not in {"encrypt", "decrypt", "create_matrix"}:
                context["error"] = "Invalid action"

        except ValueError:
            context["error"] = "Key must be numeric for this cipher"
        except Exception as ex:
            context["error"] = str(ex)

    return render_template("cipher_page.html", **context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
