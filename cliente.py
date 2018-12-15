#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Proyecto 2 - Redes de Computadoras.
Integrantes:
	Karla Fernanda Jiménez Gutierrez.
	Jonathan Suárez López.
	Alfonso Vargas Alba.
CLIENTE.
'''

import socket 
import pickle
import sys

## Número máximo de intentos.
intentos_max = 5
##Tiempo de espera de respuesta del servidor, en segundos
tiemOut = 5

if __name__ == '__main__':

	# Lista de Pokemones.
	pokemones = ["Pikachu", "Eve", "Squirtle", "Charmander","Charizard", "Pidgeotto", "Sandshrew", 
				 "Vulpix", "Seadra", "Mewtwo", "Snorlax", "Kangaskhan", "Bulbasaur"]

	if(len(sys.argv) != 3):
		print("ERROR EN PARÁMETROS\nDebes introducir la Dirección IP del servidor a conectarse y el Puerto, ejemplo:\n $python3 cliente.py 127.0.0.1 9999")
		exit(-1)

	# local host IP '127.0.0.1' 
	host = sys.argv[1]
	# Puerto al que queremos conectarnos. 9999
	port = int(sys.argv[2])
	
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
		s.settimeout(tiemOut) #Limite te tiempo para hacer la conexión
		s.connect((host,port)) # Nos conectamos al server.
		s.settimeout(None) # Ya lo quitamos porque ya nos conectamos :)
	except socket.timeout:
		print("\n\nError 40: Tiempo de espera para la conexión excedido. \n")
		exit(-1)
	except ConnectionRefusedError:
		print("Se ha rechazado la conexión del servidor. Puede que éste no esté disponible o los paramétros que introdujo sean incorrectos.")
		exit(-1)
	
	print("\n*** CONEXIÓN EXITOSA ***\n")
	try:
		usuarios_disponibles = (s.recv(1024)).decode("utf-8")
		if(usuarios_disponibles == "-"):
			print("No hay ningún usuario disponible! Espere hasta que se cierre una sesión.")
			s.close()
			exit()

		print("Antes de seguir... ¿con qué usuario quiere iniciar sesión? Estos son los disponibles:")
		print(usuarios_disponibles)
		usuario = input("\n(ESCRIBA 1, 2 ó 3 según el usuario)\n")	
		s.sendall(usuario.encode('utf-8'))

		estado_actual = "s0"

		bienvenida = s.recv(1024)
		print(bienvenida.decode("utf-8"))

		msg = pickle.dumps((10, "s1"))
		s.sendall(msg)

		while True: 
			estado_actual = pickle.loads(s.recv(4096))
			# Cargamos la tupla que nos mandaron. Revisamos en qué estado nos encontramos.
			act = estado_actual[-1]
			if act == "s2":
				pokemon_a_capt = pokemones[estado_actual[1]]
				print("¿Deseas capturar al pokemon " + pokemon_a_capt + "?")
				ans = input('\nEscoge Si/No :') 
				if ans == 'Si': 
					msg = pickle.dumps((30, 0, "s3"))
				else:
					msg = pickle.dumps((31, "s6"))
				s.sendall(msg)

			elif act == "s4":
				num_int = estado_actual[2]
				#¿Lo intenta de nuevo, o no?
				print("Intentos restantes: ", intentos_max-num_int+1)
				decision = input("\n¡No capturaste a " + pokemon_a_capt + "! Mala suerte :(.\n¿Intentar de nuevo? Si/No :\n")
				if decision == "Si":
					msg = pickle.dumps((30, num_int, "s3"))
				else:
					msg = pickle.dumps((31,"s6"))
				s.sendall(msg)
			elif act == "s5":#cuando lo capturo
				print("\n¡MUCHAS FELICIDADES, Usuario_" + usuario + " !Has capturado al Pokemon " + pokemon_a_capt + "!")
				msg = pickle.dumps((32,"s7"))
				s.sendall(msg)
			elif act == "s6": #Bye Sesión.
				print("Terminaron tus intentos o decidiste no capturar al Pokemon.\n** Terminando la sesión **")
				msg = pickle.dumps((32, "s7"))
				s.sendall(msg)
			elif act == "s7":
				print("Conexión cerrada.")
				msg = pickle.dumps((32, "s7"))
				s.sendall(msg)
				break
		s.close() 
	except EOFError:
			print("Ha habido algún error al momento de intentar cargar información recibida. Saliendo...")
			s.close()
			exit(-1)
