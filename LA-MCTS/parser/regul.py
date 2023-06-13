import sympy
from parser.regop import RegOp
from simulator.variable import Variable
from simulator.multiplex import Multiplex

class Regulation:

    def __init__(self, id:str, targets:list[Variable], formulaString:str, formulaTree:RegOp) -> None:
        self.id = id
        self.targets = targets
        self.formulaString = formulaString
        self.formulaTree = formulaTree

    def __str__(self) -> str:
        t = ""
        for tar in self.targets:
            t += str(tar)
        return (f"Regulation name : {self.id}, targets : {tar}, formulaString : {self.formulaTree.formulaTreeToStr()}")#, formulaTree : {self.formulaTree}")


    def getId(self) -> str:
        return self.id

    def getTargets(self) -> list[Variable]:
        return self.targets

    def getFormulaString(self) -> str:
        return self.formulaString

    def getFormulaTree(self) -> RegOp:
        return self.formulaTree

    def addTarget(self, target:str) -> None:
        self.targets.append(target)

    def getSympyFormula(self):
        return self.formulaTree.formulaTreeToFormulaForSympy()

    def getVariablesInFormulaTree(self):
        return self.formulaTree.getVarsInFormula()

    def transformToFormulaSimulator(self):
        return self.formulaTree.transformToFormulaSimulator()