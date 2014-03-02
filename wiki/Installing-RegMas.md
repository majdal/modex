# Instructions to install RegMAS on Debian/Ubuntu

wget http://regmas.org/snapshots/regmas_daily.tgz
tar xvzf regmas_daily.tgz
cd regmas
sudo apt-get install qt-sdk glpk zlib1g-dev
comment out documentation line in src/main.cpp (line 33)
qmake
make
MAYBE: add "-lz" to end of line starting with "LIBS =" in src/Makefile
make
./regmas
