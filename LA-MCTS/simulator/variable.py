from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulator.multiplex import Multiplex

from simulator.celeritiy import Celerity
from simulator.hybridstate import HybridState
from simulator.constants import *
from sympy import *


class Variable:

    def __init__(self, id: int, name: str, levelBound: int):
        self.id = id
        self.name = name
        self.levelBound = levelBound
        self.predecessors = []

    def __str__(self) -> str:
        return (f"Variable name : {self.name}, level bound : {self.levelBound}")

    def getId(self) -> int:
        return self.id

    def getName(self) -> str:
        return self.name

    def setName(self, newName: str) -> None:
        self.name = newName

    def getLevelBound(self) -> int:
        return self.levelBound

    def setLevelBound(self, newLevelBound: int) -> None:
        self.levelBound = newLevelBound

    def getPredecessors(self) -> list[Multiplex]:
        return self.predecessors

    def setPredecessors(self, newPredecessors: list[Multiplex]) -> None:
        self.predecessors = newPredecessors

    def addPredecessor(self, newPredecessor: Multiplex) -> None:
        self.predecessors.append(newPredecessor)

    ######################################################

    def fromVariableToSymbol(self):
        """
        This method is there to transform a variable into a symbol for sympy (it needs a symbol to evaluate an expression)
        So we create a symbol with the name of the variable.
        """
        return Symbol(self.name)

    def valueAt(self, discreteState: list[bytes]) -> int:
        """
        Returns the value of the variable at a specified discrete state.
        """
        valueOfVar = discreteState[self.getId()]
        assert self.levelBound >= valueOfVar, "The value of the variable in the discrete state must be lower or equal than the variable level bound !"
        return valueOfVar

    def isAMultiplexAResourceOfThisVariableAtDiscreteState(self, multiplex: Multiplex,
                                                           discreteState: list[bytes]) -> bool:
        """
        Is this multiplex a resource of this variable in a given discrete state
        """
        return multiplex.evaluateFormulaAtDiscreteState(discreteState)

    def resourcesOfThisVariableAtDiscreteState(self, discreteState: list[bytes]) -> list[Multiplex]:
        """
        Returns the resources (which is the list of **predecessors multiplexes** for which their formula is satisfied) of a variable at a specified discrete state.
        """
        resources = []
        for multiplex in self.predecessors:
            if self.isAMultiplexAResourceOfThisVariableAtDiscreteState(multiplex, discreteState):
                resources.append(multiplex)
        return resources

    def celerityInDiscreteState(self, celeritiesInState: list[Celerity], discreteState: list[bytes]) -> Celerity:
        """
        Returns the celerity of a variable in a specified discrete state given the list of celerities in state
        """
        for cel in celeritiesInState:
            if self.name == cel.getVariableName() and self.resourcesOfThisVariableAtDiscreteState(
                    discreteState) == cel.getResources() and discreteState[self.id] == cel.getDiscreteState():
                return cel

    def touchDelayOfThisVariableAtDiscreteState(self, celeritiesInState: list[Celerity],
                                                hybridState: HybridState) -> float:
        """
        Calculates the touch delay of a variable in a given hybrid state
        Returns the time (as a floating point)
        """
        celerityOfVariable = self.celerityInDiscreteState(celeritiesInState, hybridState.getDiscreteState())

        if celerityOfVariable.getValue() == 0.:
            return float('inf')
        elif celerityOfVariable.getValue() > 0.:
            return (FRACTIONAL_PART_TOP - hybridState.getFractionalPart()[self.getId()]) / celerityOfVariable.getValue()
        else:
            return (FRACTIONAL_PART_BOTTOM - hybridState.getFractionalPart()[
                self.getId()]) / celerityOfVariable.getValue()

    def facesAWall(self, hybridState: HybridState, celeritiesInState: list[Celerity], all_celerities: list[Celerity],
                   fractionalPart: list[float]) -> bool:
        """
        Does this variable faces a wall (internal or external) ?
        External wall : if a variable is on the edge of level 0 and its celerity is < 0 or if a variable is on the edge of its level bound and its celerity is > 0
        Internal wall : if a variable is on an edge (not an external wall) and the celerity of the current discrete state is inverse of its neibhor state (in the direction of the variable) i.e sgn(celerity_in_state) * sgn(celerity_in_neighbor_state) = -1
        Returns True or False
        """
        fractionalPart = fractionalPart[self.getId()]
        discreteState = hybridState.getDiscreteState()[self.getId()]
        celerityOfVariable = self.celerityInDiscreteState(celeritiesInState, hybridState.getDiscreteState())

        if ((fractionalPart < FRACTIONAL_PART_TOP - EPSILON) and (fractionalPart > EPSILON)):
            return False
        else:
            if ((discreteState == self.getLevelBound()) and (celerityOfVariable.getValue() > EPSILON) and (
                    abs(fractionalPart - FRACTIONAL_PART_TOP) < EPSILON)) or (
                    (discreteState == 0) and (celerityOfVariable.getValue() < EPSILON) and (fractionalPart < EPSILON)):
                return True
            else:
                if ((abs(fractionalPart - FRACTIONAL_PART_TOP) < EPSILON) and (
                        celerityOfVariable.getValue() > EPSILON)):
                    neighborDiscreteState = hybridState.neighborDiscreteState(self, 1)
                    neighborCelerity = self.celerityInDiscreteState(all_celerities, neighborDiscreteState)
                    return neighborCelerity.getValue() < EPSILON
                elif ((fractionalPart < EPSILON) and celerityOfVariable.getValue() < EPSILON):
                    neighborDiscreteState = hybridState.neighborDiscreteState(self, -1)
                    neighborCelerity = self.celerityInDiscreteState(all_celerities, neighborDiscreteState)
                    return neighborCelerity.getValue() > -EPSILON
                else:
                    return False
