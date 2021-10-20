#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import des
import pathlib
from io import open
import des3
import aes

p = 13
g = 10
b = 1

def calcularB(b,g,p):
    bMayus = (g**b)%p
    return bMayus

def calcularK(aMayus,b,p):
    k = (aMayus**b)%p
    return k

#Creando conexión
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser.bind(("", 8080))
ser.listen(1)
cli, addr = ser.accept()

print("###################### CALCULANDO K ###########################")

#Recibimos el mensaje, con el metodo recv recibimos datos. Por parametro la cantidad de bytes para recibir
aMayus = cli.recv(1024)
aMayus = int(aMayus)
print(f"Valor de A recibido del cliente: {aMayus}")

#Calculando k con valor recibido
k = calcularK(aMayus,b,p)
print(f"Valor de k: {k}")

#Se devuelve el valor de B al cliente
bMayus = calcularB(b,g,p)
print(f"Devolviendo al cliente el valor de B: {bMayus}")
msgToSend = str(bMayus)
cli.send(msgToSend.encode('ascii'))

#Descifrado con DES
print("\n###################### DESCIFRADO CON DES ###########################")
key = (k).to_bytes(8, byteorder="little")
iv = (k).to_bytes(8, byteorder="little")
msgCifrado = cli.recv(1024)
msgDescifrado = des.descifrado(key, iv, msgCifrado)

ruta = str(pathlib.Path().absolute()) + "/mensajerecibido.txt"
archivo1 = open(ruta, "w")
archivo1.write(msgDescifrado)
archivo1.close()

print(f"Mensaje descifrado: {msgDescifrado}")

#Descifrado con 3DES
print("\n###################### DESCIFRADO CON 3DES ###########################")
key = (k).to_bytes(16, byteorder="little")
msgCifrado2 = cli.recv(1024)
msgCifrado2 = msgCifrado2.decode("UTF-8")
msgDescifrado2 = des3.PrpCrypt(key).decrypt(msgCifrado2)

ruta = str(pathlib.Path().absolute()) + "/mensajerecibido2.txt"
archivo2 = open(ruta, "w")
archivo2.write(msgDescifrado2)
archivo2.close()

print(f"Mensaje descifrado: {msgDescifrado2}")


#Descifrado con AES
print("\n###################### DESCIFRADO CON AES ###########################")
key = str((k).to_bytes(8, byteorder="little"))
key = key.encode()
msgCifrado3 = cli.recv(1024)
msgCifrado3 = msgCifrado3.decode("UTF-8")
msgDescifrado3 = aes.decrypt(msgCifrado3, key)

ruta = str(pathlib.Path().absolute()) + "/mensajerecibido3.txt"
archivo2 = open(ruta, "w")
archivo2.write(msgDescifrado3)
archivo2.close()

print(f"Mensaje descifrado: {msgDescifrado3}")

#Cerramos la instancia del socket cliente y servidor
cli.close()