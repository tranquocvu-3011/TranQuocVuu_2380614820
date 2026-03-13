class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = ''.join(ch for ch in key.upper().replace('J', 'I') if ch.isalpha())

        seen = set()
        matrix_chars = []
        for ch in key:
            if ch not in seen:
                seen.add(ch)
                matrix_chars.append(ch)

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for ch in alphabet:
            if ch not in seen:
                seen.add(ch)
                matrix_chars.append(ch)

        return [matrix_chars[i:i + 5] for i in range(0, 25, 5)]

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        raise ValueError("Letter not found in Playfair matrix")

    def _normalize_text(self, text):
        return ''.join(ch for ch in text.upper().replace('J', 'I') if ch.isalpha())

    def _split_plain_pairs(self, plain_text):
        text = self._normalize_text(plain_text)
        pairs = []
        i = 0
        while i < len(text):
            first = text[i]
            second = text[i + 1] if i + 1 < len(text) else 'X'

            if first == second:
                pairs.append(first + 'X')
                i += 1
            else:
                pairs.append(first + second)
                i += 2

        if pairs and len(pairs[-1]) == 1:
            pairs[-1] += 'X'

        return pairs

    def playfair_encrypt(self, plain_text, matrix):
        pairs = self._split_plain_pairs(plain_text)
        encrypted_text = ""

        for pair in pairs:
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        text = self._normalize_text(cipher_text)
        if len(text) % 2 != 0:
            text += 'X'

        decrypted_text = ""
        for i in range(0, len(text), 2):
            pair = text[i:i + 2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        cleaned = []
        i = 0
        while i < len(decrypted_text):
            if (
                i + 2 < len(decrypted_text)
                and decrypted_text[i] == decrypted_text[i + 2]
                and decrypted_text[i + 1] == 'X'
            ):
                cleaned.append(decrypted_text[i])
                i += 2
            else:
                cleaned.append(decrypted_text[i])
                i += 1

        output = ''.join(cleaned)
        if output.endswith('X'):
            output = output[:-1]

        return output
