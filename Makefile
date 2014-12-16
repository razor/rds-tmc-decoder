all: tmcdec
tmcdec: tmcdec.c
	gcc -o tmcdec tmcdec.c
clean:
	rm -rf tmcdec
