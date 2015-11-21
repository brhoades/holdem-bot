default:
	#g++ -O3 -g specialeval.cpp SpecialKEval/src/*.cpp -o eval
	g++ -O3 -shared -fPIC -I/usr/include/python2.7/ -lpython2.7 -o specialeval.so specialeval.cpp SpecialKEval/src/*.cpp

profile: default
	valgrind --tool=callgrind --dump-instr=yes --collect-jumps=yes --simulate-cache=yes ./eval 1 2 3 4 5
	scp callgrind* ikoua:/tmp/
