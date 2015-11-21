#include <iostream>
#include "SpecialKEval/src/FiveEval.h"
#include "SpecialKEval/src/SevenEval.h"
#include <cstdlib>

using namespace std;

#define NUM_CARDS_IN_DECK 52
#define MAX_SCORE         7462

inline short* createDeck(char** argv, short* cards, const int numCards);

int main(int argc, char *argv[])
{
  if(argc < 6 || argc > 8)
  {
    cerr << "Must have 5-7 arguments." << endl;
    return 0;
  }

  // of the cards passed, first 3/5 are the table, last 2 are our cards that can't be chosen
  int numCards = argc-1;
  short cards[numCards];
  for(short i=1; i<argc; i++)
    cards[i-1] = atoi(argv[i]); 

  short* deck = createDeck(argv, cards, numCards); 
  unsigned short count=0;
  unsigned int sum=0;

  if(argc == 6)
  {
    FiveEval const eval;
    
    // get hand score possibilities for them and sum them
    for(short i=0; i<NUM_CARDS_IN_DECK-numCards; i++)
    {
      for(short j=0; j<i; j++)
      {
        sum += eval.GetRank(cards[0], cards[1], cards[2], deck[i], deck[j]);
        count++;
      }
    }
  }
  else if(argc == 7)
  {
    SevenEval const eval;
    // this isn't officially supported... emulate it by guessing the final card too
    for(short i=0; i<NUM_CARDS_IN_DECK-numCards; i++)
    {
      for(short j=0; j<i; j++)
      {
        for(short k=0; k<j; k++)
        {
          sum += eval.GetRank(cards[0], cards[1], cards[2], cards[3], 
              deck[i], deck[j], deck[k]);
          count++;
        }
      }
    }
  }
  else
  {
    SevenEval const eval;

    // get hand score possibilities for them and sum them
    for(short i=0; i<NUM_CARDS_IN_DECK-numCards; i++)
    {
      for(short j=0; j<i; j++)
      {
        sum += eval.GetRank(cards[0], cards[1], cards[2], cards[3], cards[4], 
            deck[i], deck[j]);
        count++;
      }
    }
  }

  cout << MAX_SCORE - (sum / count) << endl;

  delete[] deck;
  return 0;
}

inline short* createDeck(char** argv, short* cards, const int numCards)
{
  short* deck = new short[NUM_CARDS_IN_DECK-numCards];
  short decki=0;
 
  for(short i=0; i<NUM_CARDS_IN_DECK; i++)
  {
    bool use = true;
    for(short j=0; j<numCards; j++)
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
