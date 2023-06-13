from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from parser.regop import RegOp

from enum import Enum
from simulator.variable import Variable
from simulator.formula import Formula


from sympy import *

class RegType(Enum):
    OPERATION = "OPERATION"
    ATOME = "ATOME"


class RegOp:

    def __init__(self, typeReg:RegType, operator:str, expr1:RegOp, expr2:RegOp, var:Variable, threshold:str) -> None:
        self.regType = typeReg
        self.operator = operator
        self.expr1 = expr1
        self.expr2 = expr2
        self.var = var
        self.threshold = threshold

    def setRegType(self, newRegType:RegType) -> None:
        self.regType = newRegType

    def setOperator(self, newOperator:str) -> None:
        self.operator = newOperator
    
    def setExpr1(self, expr1:RegOp) -> None:
        self.expr1 = expr1
    
    def setExpr2(self, expr2:RegOp) -> None:
        self.expr2 = expr2
    
    def setVar(self, newVar:Variable) -> None:
        self.var = newVar
    
    def setThreshold(self, threshold:str) -> None:
        self.threshold = threshold

    def getRegType(self) -> RegType:
        return self.regType

    def getOperator(self) -> str:
        return self.operator
    
    def getExpr1(self) -> RegOp:
        return self.expr1

    def getExpr2(self) -> RegOp:
        return self.expr2
    
    def getVar(self) -> Variable:
        return self.var

    def getThreshold(self) -> str:
        return self.threshold


    def formulaTreeToStr(self) -> str:
        if self.getRegType() == RegType.ATOME:
            return self.getVar().getName() + " >= " + str(self.getThreshold())
        else:
            if self.getOperator() == '!':
                return '!' + '(' + self.getExpr1().formulaTreeToStr() + ')'
            elif self.getOperator() == '&':
                return self.getExpr1().formulaTreeToStr() + ' & ' + self.getExpr2().formulaTreeToStr()
            elif self.getOperator() == '|':
                return self.getExpr1().formulaTreeToStr() + ' | ' + self.getExpr2().formulaTreeToStr()
            else:
                raise Exception("RegOp to str conversion : Unknown operator")


    def formulaTreeToFormulaForSympy(self):
        if self.getRegType() == RegType.ATOME:
            return self.getVar().fromVariableToSymbol() >= self.getThreshold()  
        else:
            if self.getOperator() == '!':
                return Not(self.getExpr1().formulaTreeToFormulaForSympy())
            elif self.getOperator() == '&':
                return And(self.getExpr1().formulaTreeToFormulaForSympy(),self.getExpr2().formulaTreeToFormulaForSympy())
            elif self.getOperator() == '|':
                return Or(self.getExpr1().formulaTreeToFormulaForSympy(),self.getExpr2().formulaTreeToFormulaForSympy())
            else:
                raise Exception("RegOp to str conversion : Unknown operator")

    def getVarsInFormula(self) -> list[Variable]:
        if self.getRegType() == RegType.ATOME:
            return [self.getVar()]
        else:
            if self.getOperator() == '!':
                return self.getExpr1().getVarsInFormula()
            else:
                return self.getExpr1().getVarsInFormula() + self.getExpr2().getVarsInFormula()


    def transformToFormulaSimulator(self) -> Formula:
        return Formula(self.getVarsInFormula(), self.formulaTreeToFormulaForSympy())
        



