from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from variable import Variable
    
from random import randrange, seed
from itertools import product
from simulator.constants import *
from simulator.celeritiy import Celerity


def chooseAmong(listOfVariables:list[Variable], s:int=1234) -> Variable:
    """
    Returns a random item from a specified list of variables and a defined seed for reproducibility
    """
    assert len(listOfVariables) > 0, "List should not be empty to choose a random item position"
    # seed(s) # Leaving this on hinders convergence for LA-MCTS
    #print(randrange(0, len(listOfVariables)))
    return listOfVariables[randrange(0, len(listOfVariables))]


def changeFractionalPart(signOfCelerity:int) -> float:
    """
    Returns 1 if celerity is positive, 0 otherwise.
    It corresponds to the jump from one discrete state to another (reset from 1. to 0. if we jump top, reset from 0. to 1. if we jump bottom)
    """
    if signOfCelerity == 1:
        return FRACTIONAL_PART_BOTTOM
    else:
        return FRACTIONAL_PART_TOP


def generateAllDiscreteStates(variables: list[Variable]) -> list[tuple[int, int]]:
    """
    Returns the cartesian product of the range level (0 to n where n is the level bound of a var) of the variables
    """
    levelBounds = [range(var.getLevelBound()+1) for var in variables]
    allDiscreteStates = []
    for n in product(*levelBounds):
        allDiscreteStates.append(n)
    return allDiscreteStates


def generateAllCelerities(variables: list[Variable]) -> list[Celerity]:
    """
    Based on the influence graph informations i.e variables and predecessors,
    Returns the list of celerities to find.
    """
    allDiscreteStates = generateAllDiscreteStates(variables)

    listCelerities = []
    for d in allDiscreteStates:
        for var in variables:
            c = Celerity(var.getName(), var.resourcesOfThisVariableAtDiscreteState(d), d[var.getId()])
            if all(not(c.same(x)) for x in listCelerities):
                listCelerities.append(c)
    return listCelerities
