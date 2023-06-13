from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .multiplex import Multiplex


class Celerity:

    def __init__(self, variableName: str, resources: list[Multiplex], discreteState: int, value: float = 0.) -> None:
        self.variableName = variableName
        self.resources = resources
        self.discreteState = discreteState
        self.value = value

    def __str__(self) -> str:
        listOfResources = ""
        for res in self.resources:
            listOfResources += res.getName()
        return (f"C_{self.variableName}__{listOfResources}__{self.discreteState} = {self.value}")

    def getVariableName(self) -> str:
        return self.variableName

    def setVariableName(self, newVariableName: str) -> None:
        self.variableName = newVariableName

    def getResources(self) -> list[Multiplex]:
        return self.resources

    def setResources(self, newResources: list[Multiplex]) -> None:
        self.resources = newResources

    def getDiscreteState(self) -> int:
        return self.discreteState

    def setDiscreteState(self, newDiscreteState: int) -> None:
        self.discreteState = newDiscreteState

    def getValue(self) -> float:
        return self.value

    def setValue(self, newValue: float) -> None:
        self.value = newValue

    def getString(self) -> str:
        """ Get the name of the celerity """
        listOfResources = ""
        for res in self.resources:
            listOfResources += res.getName()
        return f"C_{self.variableName}__{listOfResources}__{self.discreteState}"

    def same(self, otherCelerity) -> bool:
        return self.getString() == otherCelerity.getString()
