from simulator.variable import Variable

class ElementaryPath:

    def __init__(self, transitionDelay:float, assertionElement:list[tuple[str, str, Variable]], atomDiscretePath:tuple[Variable, str]) -> None:
        self.__transitionDelay = transitionDelay
        self.__assertionElement = assertionElement
        self.__atomDiscretePath = atomDiscretePath

    def __str__(self) -> str:
        if self.getAssertionElement()[0][2] == None:
            return (f"({self.getTransitionDelay()}, {True}, {self.getAtomDiscretePath()[0].getName(), self.getAtomDiscretePath()[1]})")  
        strForMultipleAEs = ""
        for aE in self.getAssertionElement():
            strForMultipleAEs += (f"{aE[0], aE[1], aE[2].getName()},")
        return (f"({self.getTransitionDelay()}, [{strForMultipleAEs[:len(strForMultipleAEs)-1]}], {self.getAtomDiscretePath()[0].getName(), self.getAtomDiscretePath()[1]})")


    def getTransitionDelay(self) -> float:
        return self.__transitionDelay

    def getAssertionElement(self) -> list[tuple[str, str, Variable]]:
        return self.__assertionElement
    
    def getAtomDiscretePath(self) -> tuple[Variable, str]:
        return self.__atomDiscretePath


        


