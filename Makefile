.PHONY : help
help:## Muestra esta ayuda.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
	
.PHONY : clean
clean:## Borra todos los pokemos guardados de todas tus sesiones.
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive html/
	rm --force Pokedex.txt

.PHONY : cleanPoxkedex
cleanPok:## Borra todos los pokemos guardados de todas tus sesiones.
	rm --force Pokedex.txt

.PHONY : document
document:## Documenta todo el código, esta en /html/index.html.
	doxygen *.py 

.PHONY : runServ
runS:## Ejecuta el servidor.
	./src/servidor.py 

.PHONY : runCp
runCp:## Ejecuta el cliente con parametros dados H -> host P-> port.
	./src/cliente.py $(HOST) $(PORT)

.PHONY : runC
runC:## Ejecuta el cliente con parametros default.
	./src/cliente.py 127.0.0.1 9999


export PATH := $(shell pwd)/bin:$(PATH)

.PHONY : install
install: ## Instala el programa. :)
	mkdir -p ~/bin
	cp ./src/servidor.py ~/bin
	cp ./src/cliente.py ~/bin
	@echo $(PATH)

.PHONY : uninstall
uninstall: ## Desinstala el programa. :(
	rm ~/bin/cliente.py
	rm ~/bin/servidor.py
	rmdir -p ~/bin
	

