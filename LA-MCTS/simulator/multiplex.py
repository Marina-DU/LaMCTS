from __future__ import annotations
from sympy import *
from .formula import Formula

class Multiplex:

    def __init__(self, name:str, formula:Formula):
        self.name = name
        self.formula = formula

    def __str__(self) -> str:
        return (f"Multiplex name : {self.name}, formula : {self.formula}")

    def getName(self) -> str:
        return self.name

    def setName(self, newName:str) -> None:
        self.name = newName

    def getFormula(self) -> Formula:
        return self.formula

    def setFormula(self, newFormula:Formula) -> None:
        self.formula = newFormula

    ##########################################

    def evaluateFormulaAtDiscreteState(self, discreteState:list[bytes]) -> bool:
        """
        Evaluate a multiplex formula at a specified discreteState.
        Here we are using the sympy (https://www.sympy.org/en/index.html) function *subs* to evaluate the expression with each variable value in the current discrete state
        Returns True or False
        """
        setOfevaluatedVariablesAtSpecifiedDiscreteState = {}
        for i in range(0, len(self.formula.getVariables())):
            var = self.formula.getVariables()[i]
            setOfevaluatedVariablesAtSpecifiedDiscreteState[var.fromVariableToSymbol()] = var.valueAt(discreteState)
        return self.formula.getExression().subs(setOfevaluatedVariablesAtSpecifiedDiscreteState)