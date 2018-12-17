#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Proyecto 2 - Redes de Computadoras.
Integrantes:
	Karla Fernanda Jiménez Gutierrez.
	Jonathan Suárez López.
	Alfonso Vargas Alba.
SERVIDOR.
'''
import socket
from _thread import *
import threading 
import random
import pickle
import time
import os
import os.path
from PIL import Image

## Archivo que simula la base de datos.
PATH = "Pokedex.txt"
## LocalHost.
HOST = '127.0.0.1'
## Puerto a escuchar.
PORT = 9999     
## Número máximo de intentos.   
intentos_max = 5
##Tiempo de espera de conex del servidor, en segundos
tiemOut = 10

def edo3(conn,intentos_act,id_p,usuario_recv):
	if intentos_act < intentos_max:
		if(random.random() >= 0.75): # Si lo capturó. Hay 25% de probabilidades que lo haga.
			lines = open(PATH).read().splitlines()
			if usuario_recv == "1":
				lines[1] = lines[1] + " " + pokemones[id_p]
			elif usuario_recv == "2":
				lines[4] = lines[4] + " " + pokemones[id_p]
			elif usuario_recv == "3":
				lines[7] = lines[7] + " " + pokemones[id_p]

			open(PATH,'w').write('\n'.join(lines))

			img = Image.open("Pokemones/"+ pokemones[id_p] +".jpg")
			img.show()
			msg = pickle.dumps((22, id_p, "s5"))
		else:
			msg = pickle.dumps((21, id_p, (intentos_act+1), "s4"))
	else: #Ya no quedan intentos.
		msg = pickle.dumps((23, "s6"))
	conn.sendall(msg)

def cerrarSesion(conn, usuario_recv):
	msg = pickle.dumps((32, "s7"))
	print("[-] Cerrando la sesión de un cliente.")
	usuarios_disp[usuario_recv] = True
	conn.sendall(msg)

def client_thread(conn):
	'''
	Función que nos sirve para crear un nuevo thread (cliente) y manejar la conexión con éste.
	@param conn. La conexión con ese cliente.
	'''
	usuarios = "-"
	# Verificamos los usuarios que estén disponibles.
	for i in range(1, 4):
		if usuarios_disp[str(i)]:
			usuarios += "Usuario_" + str(i) + ", "

	# Se los mandamos al cliente para que sepa.
	conn.send(usuarios.encode('utf-8'))

	# El usuario con el que inicia sesión el cliente.
	usuario_recv = (conn.recv(4096)).decode('utf-8')

	# Si mandó un usuario inválido.
	if usuario_recv not in usuarios_disp:
		print("Cerrando conexión con un cliente debido a error en parámetros recibidos.")
		conn.close()
		return
	else:
		usuarios_disp[usuario_recv] = False


	msg = "¡Bienvenido a Mundo Pokemon, Usuario_" + usuario_recv + "! :)\n\n"
	conn.send(msg.encode('utf-8'))

	while True:
		#Tiempo de espera para recibir respuesta.
		conn.settimeout(tiemOut)
		try:
			# Cargamos el mensaje que envió el cliente. Vemos en qué estado estamos y a cuál nos iremos.
			msg_reci = pickle.loads(conn.recv(4096))
			conn.settimeout(None)
			estado_actual = msg_reci[-1]
			if estado_actual == "s1":
				id_p = random.randrange(len(pokemones))
				msg = pickle.dumps((20, id_p, "s2"))
				conn.sendall(msg)
			elif estado_actual == "s3":
				edo3(conn,msg_reci[1], id_p, usuario_recv)
			elif estado_actual == "s6": #Terminó la sesión
				msg = pickle.dumps((32, "s6"))
				conn.sendall(msg)
			elif estado_actual == "s7":
				cerrarSesion(conn,usuario_recv)
				break
		except socket.timeout:
			print("[Error 40] Tiempo de espera excedido. \n\t Cerrando conexión...")
			cerrarSesion(conn,usuario_recv)
			break
	conn.close()

if __name__ == '__main__':

	##  Diccionario para tener control sobre cuál usuario está conectado. 
	usuarios_disp = {"1":True, "2":True, "3":True}

	## Diccionario que tiene el nombre de los pokemons.

	pokemones = ["Pikachu", "Eve", "Squirtle", "Charmander","Charizard", "Pidgeotto", "Sandshrew", 
				 "Vulpix", "Seadra", "Mewtwo", "Snorlax", "Kangaskhan", "Bulbasaur"]

	# Si no existe un archivo que guarde los pokemones de cada usuario, lo creamos. Si no, lo usamos.
	try:
		print("Verificando existencia de la Base de datos...")
		## Variable para manejo del archivo de base de datos.
		f = open(PATH, "r")
		print("¡Existe! Procediendo a iniciar servidor.")
		f.close()
	except OSError:
		print("No existe, creando una...")
		f = open(PATH, "w+")
		f.write("POKEMONES del Usuario_1:\n- \n\nPOKEMONES del Usuario_2\n- \n\nPOKEMONES del Usuario_3\n- ")
		f.close()

	## Socket para el host y el puerto.
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	#Para reutilizar el socket aun si lo cerramos inesperadamente 
	#https://www.programcreek.com/python/example/410/socket.SO_REUSEADDR
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	

	#Tiempo de espera.
	s.settimeout(tiemOut)
	s.bind((HOST, PORT)) 
	print("Socket atado al puerto", PORT)
	s.settimeout(None)
	
	s.listen(5) 
	print("Socket escuchando...") 
	## Cadena para dar con el estado del servidor.
	estado_actual = "s0"
	
	while True:
		try:
			# Espera por aceptar una conexión.
			## Variable para confirmar la conexión.			
			conn, addr = s.accept()
			print("[-] Sesión iniciada por " + addr[0] + ":" + str(addr[1]))
			# Cliente conectado, creamos su hilo correspondiente.
			start_new_thread(client_thread, (conn,))
		except socket.timeout:
			print("Error 40: Tiempo de espera excedido. \n Cerrando conexión...")
			break
		except EOFError:
			print("Error 40: Hubó algún error al momento de intentar cargar información recibida. Continuando...")

	s.close()
