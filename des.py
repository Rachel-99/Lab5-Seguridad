import binascii
from Cryptodome.Cipher import DES
import base64

def cifrado(key,iv,msg):
    # Creo un objeto de cifrado de DES
    cipher1 = DES.new(key, DES.MODE_CFB, iv)

    # Datos necesarios
    msg = msg.encode()

    # Mensaje cifrado
    msg = cipher1.encrypt(msg)
    return [base64.standard_b64encode(msg).decode("utf-8"), msg]

def descifrado(key,iv,cifrado):
    # Creo un objeto de descifrado
    cipher2 = DES.new(key, DES.MODE_CFB, iv)

    # Proceso de descifrado
    return cipher2.decrypt(cifrado).decode()

