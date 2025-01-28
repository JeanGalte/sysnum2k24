#!/bin/sh

cd netlist-simulator
pwd
make
mv netlist_simulator ../
cd ..

cd asm
dune build
mv asm.exe ../erasm
cd ..

python3 carotte.py/carotte.py decoder.py -o decoder.net
./erasm horloge.S
rm -r rom
mkdir rom
mv out rom/prog
./netlist_simulator -c decoder.net
gcc -O2 -w out.c -o horloge -lpthread -lncurses
