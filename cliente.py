#!/usr/bin/env python

#Variables
host = 'localhost'
port = 8080

#Se importa el módulo
import socket
import pathlib
from io import open
import des
import des3
import aes

k = 0
p = 13
g = 10
a = 4

def calcularA(a,g,p):
    aMayus = (g**a)%p
    return aMayus

def calcularK(bMayus,a,p):
    k = (bMayus**a)%p
    return k

def msgEntrada():
    # lectura de archivo mensajedeentrada
    ruta = str(pathlib.Path().absolute()) + "/mensajedeentrada.txt"
    archivo = open(ruta, "r")
    mensaje = archivo.readlines()
    archivo.close()
    mensaje = mensaje[0]
    return mensaje

#Conexión con servidor
obj = socket.socket()
obj.connect((host, port))
print("Conectado al servidor")

print("###################### CALCULANDO K ###########################")
#Enviando el valor de A al servidor
aMayus = calcularA(a,g,p)
print(f"Se envía al servidor el valor de A: {aMayus}")
mens = str(aMayus)
obj.send(mens.encode('ascii'))

# mensaje recibido del servidor
bMayus = obj.recv(1024)
bMayus = int(bMayus)
print(f"Valor de B devuelto por el servidor: {bMayus}")

#Se calcula valor de k
k = calcularK(bMayus,a,p)
print(f"Valor de k: {k}")

#Mensaje de entrada
msg = msgEntrada()

#Cifrado con DES
print("\n###################### CIFRADO CON DES ###########################")
print(f"Mensaje de entrada: {msg}")
key = (k).to_bytes(8, byteorder="little")
iv = (k).to_bytes(8, byteorder="little")
msgCifrado = des.cifrado(key, iv, msg)
print(f"Mensaje cifrado: {msgCifrado[0]}")

#Enviado msg cifrado
msgCifrado = msgCifrado[1]
obj.send(msgCifrado)

#Cifrado con 3DES
print("\n###################### CIFRADO CON 3DES ###########################")
print(f"Mensaje de entrada: {msg}")
key = (k).to_bytes(16, byteorder="little") #la key debe tener 16 o 24 bits (deben ser al menos 2 llaves)
msgCifrado2 = des3.PrpCrypt(key).encrypt(msg)
print(f"Mensaje cifrado: {msgCifrado2}")

#Enviado msg cifrado
obj.send(msgCifrado2.encode('ascii'))


#Cifrado con AES
print("\n###################### CIFRADO CON AES ###########################")
print(f"Mensaje de entrada: {msg}")
key = str((k).to_bytes(8, byteorder="little"))
key = key.encode() 
msgCifrado3 = aes.encrypt(msg, key)
print(f"Mensaje cifrado: {msgCifrado3}")

#Enviado msg cifrado
obj.send(msgCifrado3.encode('ascii'))

#Cerramos la instancia del objeto servidor
obj.close()

#Imprimimos la palabra Adios para cuando se cierre la conexion
print("\nConexión cerrada")