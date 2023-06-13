from __future__ import annotations
from inspect import trace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulator.formula import Formula

from os import name
from simulator.celeritiy import Celerity
from simulator.hybridstate import HybridState
from simulator.multiplex import Multiplex
from simulator.variable import Variable
from simulator.utils import *
from simulator.constants import *
import random


class Simulator:
    
    def __init__(self, variables:list[Variable], initialHybridState:HybridState, KB=None) -> None:
        self.__variables = variables
        self.__initialHybridState = initialHybridState

        self.__allCelerities = generateAllCelerities(variables)
        self.__trace = []

        self.__KB = KB

        self.__blockages = 0
        self.__badTransitions = 0
        self.__exitPoints = 0

    def incrementNbrExitPoints(self) -> None:
        self.__exitPoints +=1
    
    def getNbrExitPoints(self) -> int:
        return self.__exitPoints

    def incrementBlockagesCount(self) -> None:
        self.__blockages +=1

    def getBlockagesCount(self) -> int:
        return self.__blockages
    
    def incrementBadTransitions(self) -> None:
        self.__badTransitions += 1

    def getBadTransitionsCount(self) -> int:
        return self.__badTransitions

    def getKB(self):
        return self.__KB

    def getVariables(self) -> list[Variable]:
        return self.__variables

    def getInitialHybridState(self) -> HybridState:
        return self.__initialHybridState

    def setInitialHybridState(self, newInitialHybridState:HybridState) -> None:
        self.__initialHybridState = newInitialHybridState

    def getAllCelerities(self) -> list[Celerity]:
        return self.__allCelerities

    def getTrace(self) -> list[tuple[float, HybridState]]:
        return self.__trace

    def resetTrace(self):
        self.__trace = []

    def reset(self):
        self.__trace = []
        self.__blockages = 0
        self.__badTransitions = 0
        self.__exitPoints = 0

    def addToTrace(self, path:list[tuple[float, HybridState]]) -> None:
        self.__trace  = self.__trace + path

    def setCeleritiesValue(self, celeritiesValues:list[float]) -> None:
        for i in range(len(self.__allCelerities)):
            self.__allCelerities[i].setValue(celeritiesValues[i])


    def getNumberOfExitPointsInTrace(self) -> int:
        nb=0
        if(len(self.getTrace()) > 1):
            #if self.getInitialHybridState().getDiscreteState() != self.getTrace()[0][1].getDiscreteState():
            #    nb+=1
            for i in range(0, len(self.__trace)-1):
                if self.__trace[i][1].isAnExitPoint(self.__trace[i+1][1]):
                    nb+=1
            #if self.__trace[i][1].isAnExitPoint(self.__trace[i-1][1]):
            #    nb+=1      
        
        return nb


    def simulateUntilTime(self, maximumTime: float, initialTime: float, previousTime: float, variables: list[Variable], hybridState: HybridState, all_celerities: list[Celerity]) -> list[tuple[float, HybridState]]:
        """
        Launches the simulation based on the influence graph knowledges.

        INPUT:
        variables : list of all variables of influence graph
        hybridState : current hybrid state
        all_celerities : list of all celerities (initially generated thx to generateAllCelerities())
        initialTime : initial time when this method is called (as it is a recursive one, it will become the new calculated time etc...)
        maximumTime : the termination criterion is the time so it will stop when this threshold is exceeded
        trace : it corresponds to the actual trace : a trace is a list of (time, hybrid state)
        previousTime : t-1 (it is initialTime at next recursivity)

        OUTPUT: the trace calculated at initialTime
        """
        if (initialTime == previousTime) and (initialTime > 0.):
            self.addToTrace([(maximumTime, (hybridState))])
        else:
            if not((abs(initialTime - maximumTime) < EPSILON) or (initialTime > maximumTime)):
                jumpVarsAndContinuousTransition = hybridState.jumpingVariablesAndContinuousTransition(
                    variables, variables, all_celerities, hybridState.getFractionalPart(), initialTime)
                allContinuousTransitions = [i[1]
                                            for i in jumpVarsAndContinuousTransition]
                reversedList = jumpVarsAndContinuousTransition[::-1]
                jumpingVariables = reversedList[0][0]
                continuousTransition = reversedList[0][1]
                newTime = continuousTransition[0]
                newHybridState = continuousTransition[1]
                if len(jumpingVariables) == 0:  # not len(liste) also works
                    self.addToTrace([(maximumTime, newHybridState)])
                else:
                    chosenVariable = chooseAmong(jumpingVariables)
                    celertityOfChosenVariable = chosenVariable.celerityInDiscreteState(
                        all_celerities, newHybridState.getDiscreteState())
                    if celertityOfChosenVariable.getValue() > EPSILON:
                        celeritySignOfChosenVariable = 1
                    else:
                        celeritySignOfChosenVariable = -1
                    nextDiscreteState = newHybridState.neighborDiscreteState(
                        chosenVariable, celeritySignOfChosenVariable)
                    nextFractionalPart = newHybridState.neighborFractionalPart(
                        chosenVariable, celeritySignOfChosenVariable)
                    self.addToTrace(allContinuousTransitions)
                    self.simulateUntilTime(maximumTime, newTime, initialTime, variables, HybridState(nextDiscreteState, nextFractionalPart), all_celerities)


    def simulation(self, allCelerities:list[Celerity]=None, initialTime:float=0., debug:bool=False):
        """
        Launches the simulation of a trace based on influence graph knowledges.

        The idea is to have a trajectory in the form of : 0-[initial hybrid state] 1-[slide hybrid stateS if any] 2-[exit hybrid state] 3-[entry hybrid state](loop to 1-) 4-[final hybrid state]
        """

        # INITIALIZATION # 
        ## 1. Get information about the biological knowledge
        BK_time, BK_gliss, BK_gliss_entity, BK_gliss_top_bottom, BK_disc_trans, _, _ = self.getKB()

        nbExitPointMax = len(BK_disc_trans)
        variables = self.getVariables()
        initialHybridState = self.getInitialHybridState()
        if allCelerities is None:
            allCelerities = self.getAllCelerities()
        
        ##3. information to be saved depending on the state of the process
        currentTime = initialTime
        currentHybridState = initialHybridState
        self.addToTrace([(currentTime, currentHybridState)]) 

        # MAIN LOOP #
        #1. The stoppping condition is one cycle i.e. a number max of exit points
        while self.getNbrExitPoints() < nbExitPointMax:
            
            #debug if necessary
            if debug:
                if(len(self.getTrace()) > 0):
                    for e in self.getTrace():
                        print(e[0], " ", e[1])
                    #print(self.getTrace()[-1][0], ' ', self.getTrace()[-1][1])
                print("Nb exit points: ", self.getNbrExitPoints())
                print("Nb blockages: ", self.getBlockagesCount())
                print("Nb bad trans: ", self.getBadTransitionsCount())

            #1. get infos about continuous trajectory inside the actual discrete state
            jumpVarsAndContinuousTransition = currentHybridState.jumpingVariablesAndContinuousTransition(
                    variables, variables, allCelerities, currentHybridState.getFractionalPart(), currentTime)
            allContinuousTransitions = [i[1] for i in jumpVarsAndContinuousTransition]
            self.addToTrace(allContinuousTransitions)
            #4. Extract necessary information
            jumpingVariables, (newTime, newHybridState) = jumpVarsAndContinuousTransition[::-1][0]
            if len(jumpingVariables) == 0:
                #print("BLOCKAGE")
                #1. increment the counter of blockages and of exit points since a blockage is an exit point
                self.incrementBlockagesCount()
                #newTime is the same as before we just restart the trace away immediately
                newHybridState = HybridState(BK_disc_trans[self.getNbrExitPoints() % len(BK_disc_trans)], newHybridState.getFractionalPart())
            else:
                #5. sort the jumping variables (same seed for same list)
                jumpingVariables.sort(key=lambda x: x.getName())
                #6. choose one variable among the list of variables
                chosenVariable = chooseAmong(jumpingVariables)
                #7. find the celerity of the chosen variable in the actual discrete state
                celertityOfChosenVariable = chosenVariable.celerityInDiscreteState(allCelerities, newHybridState.getDiscreteState())
                if celertityOfChosenVariable.getValue() > EPSILON:
                    celeritySignOfChosenVariable = 1
                else:
                    celeritySignOfChosenVariable = -1
                #Even if it is a viable trajectory we must check if it goes in the right discrete state (same as the one specified by BK)
                nextDiscreteState = newHybridState.neighborDiscreteState(
                    chosenVariable, celeritySignOfChosenVariable)
                nextDiscreteStateAccordingToBK = self.getNbrExitPoints() % len(BK_disc_trans)
                #print("NDX :", BK_disc_trans[nextDiscreteStateAccordingToBK])
                #simulated trace is not going to the right discrete state
                if nextDiscreteState != BK_disc_trans[nextDiscreteStateAccordingToBK]:
                    #print("BAD TRANS")
                    #increment bad transition
                    self.incrementBadTransitions()
                    newHybridState = HybridState(BK_disc_trans[nextDiscreteStateAccordingToBK], currentHybridState.getFractionalPart())
                else:
                    #print("NO BAD TRANS")
                    nextFractionalPart = newHybridState.neighborFractionalPart(chosenVariable, celeritySignOfChosenVariable)
                    newHybridState = HybridState(nextDiscreteState, nextFractionalPart)
            self.addToTrace([(newTime, newHybridState)]) 
            #in this case we increment the number of exit points
            self.incrementNbrExitPoints()
            currentTime = newTime
            currentHybridState = newHybridState

        #to get display the next hybrid state
        if not(currentHybridState.isTheSameAs(self.getTrace()[-1][1])):
           self.addToTrace([(currentTime, currentHybridState)]) 