#include <iostream>
#include "SpecialKEval/src/FiveEval.h"
#include "SpecialKEval/src/SevenEval.h"
#include <cstdlib>

using namespace std;

#define NUM_CARDS_IN_DECK 52
#define MAX_SCORE         7462

int* createDeck(char** argv, int* cards, const int numCards);

int main(int argc, char *argv[])
{
  if(argc != 6 && argc != 8)
  {
    cerr << "Must have 5 or 7 arguments." << endl;
    return 0;
  }

  // of the cards passed, first 3/5 are the table, last 2 are our cards that can't be chosen
  int* cards = new int[argc-1];
  for(int i=1; i<argc; i++)
    cards[i-1] = atoi(argv[i]); 

  int* deck = createDeck(argv, cards, argc-1); 
  int count=0;
  unsigned int sum=0;

  if(argc == 6)
  {
    FiveEval const eval;
    
    // get hand score possibilities for them and sum them
    for(int i=0; i<NUM_CARDS_IN_DECK-argc+1; i++)
    {
      for(int j=0; j<i; j++)
      {
        sum += eval.GetRank(cards[0], cards[1], cards[2], deck[i], deck[j]);
        count++;
      }
    }
  }
  else
  {
    SevenEval const eval;

    // get hand score possibilities for them and sum them
    for(int i=0; i<NUM_CARDS_IN_DECK-argc+1; i++)
    {
      for(int j=0; j<i; j++)
      {
        sum += eval.GetRank(cards[0], cards[1], cards[2], cards[3], cards[4], 
            deck[i], deck[j]);
        count++;
      }
    }
  }

  cout << MAX_SCORE - (sum / count) << endl;

  delete deck;
  delete cards;
  return 0;
}

inline int* createDeck(char** argv, int* cards, const int numCards)
{
  int* deck = new int[NUM_CARDS_IN_DECK-numCards];
  int decki=0;
 
  for(int i=0; i<NUM_CARDS_IN_DECK; i++)
  {
    bool use = true;
    for(int j=0; j<numCards; j++)
    {
      if(i == cards[j])
      {
        use=false;
        break;
      }
    }
    if(use)
      deck[decki++] = i;
  }

  return deck;
}
