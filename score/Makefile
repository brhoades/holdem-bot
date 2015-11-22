PYFLAGS=$(shell python2-config --cflags)
PYLDFLAGS=$(shell python2-config --ldflags)

default:
	#g++ -O3 -g specialeval.cpp SpecialKEval/src/*.cpp -o eval
	g++ -O3 -fPIC -shared $(PYFLAGS) -o specialeval.so -Bstatic $(PYLDFLAGS) specialeval.cpp SpecialKEval/src/*.cpp

profile: default
	valgrind --tool=callgrind --dump-instr=yes --collect-jumps=yes --simulate-cache=yes ./eval 1 2 3 4 5
	scp callgrind* ikoua:/tmp/
