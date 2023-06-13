from __future__ import annotations
from simulator.variable import Variable


class Formula:

    def __init__(self, variables:list[Variable], expression) -> None:
        self.variables = variables
        self.expression = expression

    def __str__(self) -> str:
        return (f"Formula : {self.expression}")

    def getVariables(self) -> list[Variable]:
        return self.variables

    def setVariables(self, newVariables:list[Variable]) -> None:
        self.variables = newVariables

    def getExression(self):
        return self.expression

    def setExpression(self, newExpression) -> None:
        self.expression = newExpression
