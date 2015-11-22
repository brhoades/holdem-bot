#include "SpecialKEval/src/FiveEval.h"
#include "SpecialKEval/src/SevenEval.h"
#include <cstdlib>
#include <Python.h>
#include <algorithm>

using namespace std;

#define NUM_CARDS_IN_DECK 52
#define MAX_CARDS_IN      7
#define MAX_SCORE         7462

inline short* createDeck(short* cards, const short numCards);
static inline PyObject* specialeval_get_score(PyObject* self, PyObject* args);

static PyMethodDef ScoreMethods[] = {
    {"get_score", specialeval_get_score, METH_VARARGS,
     "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initspecialeval(void)
{
  PyObject *m;

  m = Py_InitModule("specialeval", ScoreMethods);
  if (m == NULL)
    return;
}

static inline PyObject* specialeval_get_score(PyObject* self, PyObject* args)
{
  short cards[MAX_CARDS_IN];
  short numCards = 7;

  fill_n(cards, MAX_CARDS_IN, -1);

  if(PyArg_ParseTuple(args, "iiiii|ii", &cards[0], &cards[1], &cards[2], 
     &cards[3], &cards[4], &cards[5], &cards[6]))
  {
    for(short i=0; i<MAX_CARDS_IN; i++)
    {
      if(cards[i] <= 0)
      {
        numCards = i; 
        break;
      }
      else
        cards[i]--; // python offsets them by one so we can see the end of our arguments easier
    }
  }
  else
    return NULL;

  short* deck = createDeck(cards, numCards); 
  unsigned short count=0;
  unsigned int sum=0;
  static const FiveEval eval5;
  static const SevenEval eval7;
    

  if(numCards == 5)
  {
    // get hand score possibilities for them and sum them
    for(short i=0; i<NUM_CARDS_IN_DECK-numCards; i++)
    {
      for(short j=0; j<i; j++)
      {
        sum += eval5.GetRank(cards[0], cards[1], cards[2], deck[i], deck[j]);
        count++;
      }
    }
    fprintf(stderr,"EVAL: 5 cards\n");
  }
  else if(numCards == 6)
  {
    // this isn't officially supported... emulate it by guessing the final card too
    for(short i=0; i<NUM_CARDS_IN_DECK-numCards; i++)
    {
      for(short j=0; j<i; j++)
      {
        for(short k=0; k<j; k++)
        {
          sum += eval7.GetRank(cards[0], cards[1], cards[2], cards[3], 
              deck[i], deck[j], deck[k]);
          count++;
        }
      }
    }
    fprintf(stderr,"EVAL: 6 cards\n");
  }
  else
  {
    // get hand score possibilities for them and sum them
    for(short i=0; i<NUM_CARDS_IN_DECK-numCards; i++)
    {
      for(short j=0; j<i; j++)
      {
        sum += eval7.GetRank(cards[0], cards[1], cards[2], cards[3], cards[4], 
            deck[i], deck[j]);
        count++;
      }
    }
    fprintf(stderr,"EVAL: 7 cards\n");
  }

  fprintf(stderr,"Count %i\n", count);

  delete[] deck;
  return Py_BuildValue("i", MAX_SCORE - (sum / count));
}

inline short* createDeck(short* cards, const short numCards)
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
