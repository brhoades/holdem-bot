#include "SpecialKEval/src/FiveEval.h"
#include "SpecialKEval/src/SevenEval.h"
#include <cstdlib>
#include <Python.h>

using namespace std;

#define NUM_CARDS_IN_DECK 52
#define MAX_CARDS_IN      7
#define MAX_SCORE         7462

inline short* createDeck(short* cards, const int numCards);
static PyObject* specialeval_get_score(PyObject* self, PyObject* args);

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

static PyObject* specialeval_get_score(PyObject* self, PyObject* args)
{
  short cards[MAX_CARDS_IN] = {-1};
  int numCards = 7;
  if(PyArg_ParseTuple(args, "iiiii|ii", &cards[0], &cards[1], &cards[2], 
     &cards[3], &cards[4], &cards[5], &cards[6]))
  {
    for(short i=5; i<MAX_CARDS_IN; i++)
    {
      if(cards[i] == -1)
        numCards = i; 
    }
  }
  else
    return NULL;

  short* deck = createDeck(cards, numCards); 
  unsigned short count=0;
  unsigned int sum=0;

  if(numCards == 6)
  {
    static FiveEval const eval;
    
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
  else if(numCards == 7)
  {
    static SevenEval const eval;
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
    static SevenEval const eval;

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

  delete[] deck;
  return Py_BuildValue("i", MAX_SCORE - (sum / count));
}

inline short* createDeck(short* cards, const int numCards)
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
