#include <iostream>
#include "SpecialKEval/src/FiveEval.h"
#include "SpecialKEval/src/SevenEval.h"
#include <cstdlib>

using namespace std;

int main(int argc, char *argv[])
{
  if(argc != 6 && argc != 8)
  {
    cerr << "Must have 5 or 7 arguments." << endl;
    return 0;
  }

  if(argc == 6)
  {
    FiveEval const eval;

    cout << eval.GetRank(atoi(argv[1]), atoi(argv[2]), atoi(argv[3]), atoi(argv[3]), 
        atoi(argv[5])) << endl;
    return 0;
  }

  SevenEval const eval;

  cout << eval.GetRank(atoi(argv[1]), atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), 
      atoi(argv[5]), atoi(argv[6]), atoi(argv[7])) << endl;
  return 0;
}
