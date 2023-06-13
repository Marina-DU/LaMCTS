from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulator.variable import Variable
    from simulator.celeritiy import Celerity

from simulator.utils import *
from simulator.constants import *


class HybridState:

    def __init__(self, discreteState: list[bytes], fractionalPart: list[float]) -> None:
        self.discreteState = discreteState
        self.fractionalPart = fractionalPart

    def __str__(self) -> str:
        return (f"hybridState = ({self.discreteState}, {self.fractionalPart})")

    def getDiscreteState(self) -> list[bytes]:
        return self.discreteState

    def getFractionalPart(self) -> list[float]:
        return self.fractionalPart

    def setDiscreteState(self, newDiscreteState: list[bytes]) -> None:
        self.discreteState = newDiscreteState

    def setFractionalPart(self, newFractionalPart: list[float]) -> None:
        self.fractionalPart = newFractionalPart

    ######

    def neighborDiscreteState(self, variable: Variable, direction: int) -> list[bytes]:
        """
        Returns the neighbor discrete state in the direction (+1/-1) of the variable
        """
        assert direction == 1 or direction == -1, "Direction should only be +1 or -1 integers"
        newDiscreteState = [self.discreteState[i] + direction if i == variable.getId() else self.discreteState[i] for i
                            in range(len(self.discreteState))]
        return newDiscreteState

    def neighborFractionalPart(self, variable: Variable, signOfCelerity: int) -> list[float]:
        """
        Depending of the sign of the celerity of the variable, returns the new fractionalPart (see changeFractionalPart for more information)
        """
        newFractionalPart = [changeFractionalPart(signOfCelerity) if i == variable.getId() else self.fractionalPart[i]
                             for i in range(len(self.fractionalPart))]
        return newFractionalPart

    def getCeleritiesInDiscreteState(self, variables: list[Variable], all_celerities: list[Celerity]) -> list[Celerity]:
        """
        Returns the list of celerities involved in a specified discrete state
        """
        listOfCeleritiesInCurrentDiscreteState = []
        for var in variables:
            listOfCeleritiesInCurrentDiscreteState.append(
                var.celerityInDiscreteState(all_celerities, self.discreteState))
        return listOfCeleritiesInCurrentDiscreteState

    def calculateTouchDelayOfVariables(self, variables: list[Variable], celeritiesInState: list[Celerity],
                                       fractionalPart: list[float]) -> list[tuple[Variable, float]]:
        """
        Create a list of tuple including each variable and its touch delay associated in the discrete state
        """
        listOfTouchDelay = []
        for var in variables:
            listOfTouchDelay.append((var, var.touchDelayOfThisVariableAtDiscreteState(celeritiesInState,
                                                                                      HybridState(self.discreteState,
                                                                                                  fractionalPart))))
        return listOfTouchDelay

    def firstChangingEntities(self, touchDelayList: list[tuple[Variable, float]]) -> tuple[list[Variable], float]:
        """
        Searches for ALL variables that touch their edge, first (<epsilon).

        INPUT :
        touchDelayList is a tuple in the form (variable, touch delay)

        OUTPUT:
        list in the form ([listOfVariables], float) i.e multiple variables could have the same (< epsilon) touch delay 

        Returns the list of variables and their corresponding touch delay
        """
        assert len(touchDelayList) > 0, "List of touch delay should not be empty !"

        var = touchDelayList[0][0]
        touchDelayMin = touchDelayList[0][1]
        if len(touchDelayList) == 1:
            return ([var], touchDelayMin)
        else:
            tailOfTouchDelayList = touchDelayList[1:]
            (listVariables, newTouchDelay) = self.firstChangingEntities(tailOfTouchDelayList)
            if ((abs(newTouchDelay - touchDelayMin) < EPSILON)):
                return ([var] + listVariables, newTouchDelay)
            elif (touchDelayMin < newTouchDelay - EPSILON):
                return ([var], touchDelayMin)
            else:
                return (listVariables, newTouchDelay)

    def getSlidingVariables(self, all_celerities: list[Celerity], celeritiesInState: list[Celerity],
                            variables: list[Variable], fractionalPart: list[float]) -> list[Variable]:
        """
        Identifies and returns all the sliding variables in the current hybrid state
        """
        slidingVariables = []
        for var in variables:
            if var.facesAWall(self, celeritiesInState, all_celerities, fractionalPart):
                slidingVariables.append(var)
        return slidingVariables

    def buildNewFractionalPartInCurrentDiscreteState(self, variables: list[Variable], celeritiesInState: list[Celerity],
                                                     first: tuple[list[Variable], float],
                                                     slidingVariables: list[Variable], fractionalPart: list[float]) -> \
    list[float]:
        """
        Build the new hybrid state (new fractional part) in the current discrete state

        INPUT :
        variables : list of all variables,
        all_celerities : all the celerities,
        first : the first changing entities set and their minimum touch delay
        slidingVariables : the sliding entities

        Returns the new calculated fractional part
        """
        newFractionalPart = [0. for _ in range(
            len(variables))]  # could be initialized as an empty list but it allows to not have the variables list ordered !
        for var in variables:
            celerityOfVarInDiscreteState = var.celerityInDiscreteState(celeritiesInState, self.discreteState)
            listOfFirstEntities = first[0]
            if var in listOfFirstEntities or var in slidingVariables:
                if celerityOfVarInDiscreteState.getValue() > EPSILON:
                    newFractionalPart[var.getId()] = FRACTIONAL_PART_TOP
                else:
                    newFractionalPart[var.getId()] = FRACTIONAL_PART_BOTTOM
            else:
                newFractionalPart[var.getId()] = fractionalPart[var.getId()] + (
                            celerityOfVarInDiscreteState.getValue() * first[1])

        return newFractionalPart

    def continuousLineSegment(self, variables: list[Variable], listOfVariables: list[Variable],
                              all_celerities: list[Celerity],
                              fractionalPart: list[float]) -> tuple(float, list[float]):
        """
        Identify the continuous transition in the current discrete state

        Returns the first set and the new fractional part built from the current discrete state
        """
        celeritiesInState = self.getCeleritiesInDiscreteState(variables, all_celerities)
        slidingVariables = self.getSlidingVariables(all_celerities, celeritiesInState, variables, fractionalPart)
        touchDelayList = self.calculateTouchDelayOfVariables(listOfVariables, celeritiesInState, fractionalPart)
        firstEntitiesAndTouchMin = self.firstChangingEntities(touchDelayList)

        return (firstEntitiesAndTouchMin,
                self.buildNewFractionalPartInCurrentDiscreteState(variables, celeritiesInState,
                                                                  firstEntitiesAndTouchMin, slidingVariables,
                                                                  fractionalPart))

    def jumpingVariablesAndContinuousTransition(self, variables: list[Variable], listOfVariables: list[Variable],
                                                all_celerities: list[Celerity], fractionalPart: list[float],
                                                time: float) -> list[tuple[list[Variable], tuple[float, HybridState]]]:
        """
        Identify and returns the jumping variables and the continuous transition inside the current discrete state.        
        """
        lineSegment = self.continuousLineSegment(variables, listOfVariables, all_celerities, fractionalPart)
        listOfFirstEntities, touchDelayMinimum = lineSegment[0]
        newFractionalPart = lineSegment[1]

        celeritiesInState = self.getCeleritiesInDiscreteState(listOfVariables, all_celerities)
        slidingVariables = self.getSlidingVariables(all_celerities, celeritiesInState, listOfFirstEntities,
                                                    newFractionalPart)
        jumpingVariables = list(set(listOfFirstEntities) - set(slidingVariables))

        varNotSliding = list(set(listOfVariables) - set(slidingVariables))

        # check if all variables in lineSegment are slidin variables
        if all(var in slidingVariables for var in listOfFirstEntities) and len(varNotSliding) != 0:
            return [(jumpingVariables, ((touchDelayMinimum + time), HybridState(self.discreteState,
                                                                                newFractionalPart)))] + self.jumpingVariablesAndContinuousTransition(
                variables, varNotSliding, all_celerities, newFractionalPart, time + touchDelayMinimum)
        else:
            return [(jumpingVariables, ((touchDelayMinimum + time), HybridState(self.discreteState, newFractionalPart)))]


    def isTheSameAs(self, hybridState: HybridState) -> bool:
        """
        Is it the same hybridState ?
        """
        if self.getDiscreteState() == hybridState.getDiscreteState() and self.getFractionalPart() == hybridState.getFractionalPart():
            return True
        return False


    def isAnExitPoint(self, nextHybridState: HybridState) -> bool:
        if nextHybridState.getDiscreteState() != self.getDiscreteState():
            return True
        return False
