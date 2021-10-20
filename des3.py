import base64

from Crypto.Cipher import DES3

# BS = DES3.block_size   # pkcs7padding
BS = 8  # pkcs5padding

def pad(s):
    """relleno"""
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')


def unpad(s):
    "" "Eliminar caracteres de relleno" ""
    return s[0:-ord(s[-1])]


class PrpCrypt:
    def __init__(self, key):
        self.key = key
        self.mode = DES3.MODE_ECB

    def encrypt(self, text):
        text = pad(text.encode('utf-8'))
        cryptor = DES3.new(self.key, self.mode)  # Si hay iv, agregue el parámetro iv aquí
        # Complemento de menos de 16, 32, 64 bits 0
        x = len(text) % 8
        if x != 0:
            text = text + "\0" * (8 - x)
        self.cipher_text = cryptor.encrypt(text)
        return base64.standard_b64encode(self.cipher_text).decode("utf-8")

    def decrypt(self, text):
        cryptor = DES3.new(self.key, self.mode)
        de_text = base64.standard_b64decode(text.encode("utf-8"))
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')
        out = unpad(st)
        return out

