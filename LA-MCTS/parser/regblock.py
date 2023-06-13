from parser.regul import Regulation
from parser.regop import RegOp

class RegBlock:

    def __init__(self) -> None:
        self.regs = []
        self.targets = set()

    def getRegs(self) -> list[Regulation]:
        return self.regs

    def getRegWithId(self, id:str) -> Regulation:
        for reg in self.regs:
            if reg.getId() == id:
                return reg
        return None

    def existsReg(self, regId:str) -> bool:
        return self.getRegWithId(regId) != None

    def addReg(self, id:str, targets:list[str], formulaString:str, operation:RegOp) -> None:
        self.targets.update(targets)
        self.regs.append(Regulation(id, targets, formulaString, operation))