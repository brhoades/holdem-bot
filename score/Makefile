default:
	g++ -O3 -g specialeval.cpp SpecialKEval/src/*.cpp -o eval

profile: default
	valgrind --tool=callgrind --dump-instr=yes --collect-jumps=yes --simulate-cache=yes ./eval 1 2 3 4 5
	scp callgrind* ikoua:/tmp/
