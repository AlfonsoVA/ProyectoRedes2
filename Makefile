clean:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive html/
	rm --force Pokedex.txt

cleanPoxkedex:
	rm --force Pokedex.txt

document:
	doxygen *.py 

runServ:
	python3 servidor.py 

#ejecuta el cliente con parametros dados H -> host P-> port
runClientHP:
	./cliente.py $(HOST) $(PORT)

#ejecuta el cliente con parametros default
runClient:
	./cliente.py 127.0.0.1 9999
