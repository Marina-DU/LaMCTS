from sympy.core.symbol import var
from simulator.variable import Variable
from parser.grammar.IGParser import IGParser

class VarBlock:

    def __init__(self) -> None:
        self.data = []

    def getData(self) -> list[Variable]:
        return self.data

    def filterVar(self, varId:str) -> int:
        n = 0
        for v in self.getData():
            if v.getName() == varId:
                n+=1
        return n

    def existsVar(self, varId:str) -> bool:
        varCount = self.filterVar(varId)
        if varCount > 1:
            print("Var " + varId + ": " + varCount + " var with this id.")
        return varCount == 1

    def addVar(self, id:str, valMax:int) -> None:
        self.data.append(Variable(len(self.data), id, valMax))

    def getVarWithId(self, id:str) -> Variable:
        for var in self.data:
            if var.getName() == id:
                return var
        return None