from parser.elementarypath import ElementaryPath
from parser.grammar.IGVisitor import IGVisitor
from parser.grammar.IGParser import IGParser
from parser.regop import RegOp, RegType
from parser.regblock import RegBlock
from parser.hybridhoareblock import HybridHoareBlock

from parser.varblock import VarBlock
from simulator.hybridstate import HybridState
from simulator.variable import Variable
from simulator.multiplex import Multiplex

import simulator.constants

from antlr4 import *

class Visitor(IGVisitor):

    def __init__(self) -> None:
        self.errorCounter = 0
        self.varBlock = VarBlock()
        self.regBlock = RegBlock()
        self.hybridHoareBlock = HybridHoareBlock()

    def getVarBlock(self) -> VarBlock:
        return self.varBlock

    def getRegBlock(self) -> RegBlock:
       return self.regBlock
    
    def getHybridHoareBlock(self) -> HybridHoareBlock:
        return self.hybridHoareBlock


    # *** Utilities ***
    def getLineNumber(self, ctx:ParserRuleContext) -> str:
        return "Line " + str(ctx.start.__getattribute__("line")) + " Column " + str(ctx.start.__getattribute__("column"))
    
    
    def getErrorCounter(self):
        return self.errorCounter

    def newErrorToPrint(self, message):
        self.errorCounter+=1
        print("\n > SMB PARSER error. " + message)

    # *** Visitors ***
    def visitProg(self, ctx:IGParser.ProgContext):
        if ctx.KCYCLIC():
            self.getHybridHoareBlock().setCyclic()
        return self.visitChildren(ctx)

    # *** Var Visitors ***
    def visitVar_decl(self, ctx:IGParser.Var_declContext) -> str:
        if self.varBlock.existsVar(str(ctx.getChild(0))):
            self.newErrorToPrint(self.getLineNumber(ctx) + " var \"" + str(ctx.getChild(0)) + "\" is already declared.") 
        min = int(str(ctx.NUM(0)))
        max = int(str(ctx.NUM(1)))
        if min > max:
            self.newErrorToPrint(self.getLineNumber(ctx) + " Bad bounds for var \"" + str(ctx.getChild(0)) + "\"")
        self.varBlock.addVar(str(ctx.getChild(0)), max)
        return self.visitChildren(ctx)
    

    # *** Reg Visitors ***
    def visitReg_decl(self, ctx:IGParser.Reg_declContext) -> str:
        targets = ctx.ID()
        del targets[0]

        # mult name : print(ctx.ID(0))
        # target var : print(ctx.ID(1))

        if self.regBlock.existsReg(str(ctx.ID(0))):
            self.newErrorToPrint(self.getLineNumber(ctx) + " REG block : reg SBMname \"" + str(ctx.ID(0)) + "\" is already declared.")
        if self.varBlock.existsVar(str(ctx.ID(0))):
            self.newErrorToPrint(self.getLineNumber(ctx) + " REG block : reg SBMname \"" + str(ctx.ID(0)) + "\" already exists for a variable.")

        for i in range(len(targets)):
            targets[i] = str(targets[i])
            #print(targets[i])
            if not(self.varBlock.existsVar(targets[i])):
                self.newErrorToPrint(self.getLineNumber(ctx) + " REG block : reg target \"" + str(ctx.ID(1)) + "\" is not declared as a var.")

        firstOperation = self.createREGfrom(ctx.reg_expr())
        #self.regBlock.addReg(str(ctx.ID(0)), [self.getVarBlock().getVarWithId(str(ctx.ID(1)))], "", firstOperation)
        self.regBlock.addReg(str(ctx.ID(0)), targets, "", firstOperation)

        for i in range(len(targets)):
            #we add here the predecessors
            self.varBlock.getVarWithId(targets[i]).addPredecessor(Multiplex(str(ctx.ID(0)), self.regBlock.getRegWithId(str(ctx.ID(0))).transformToFormulaSimulator()))

        return self.visitChildren(ctx)

    def createREGfrom(self, ctx:IGParser.Reg_exprContext) -> RegOp:
        name = type(ctx).__name__
        #bracketsContext
        if (name == "Expr_bracketsContext"):
            return self.createREGfrom(ctx.reg_expr())
        #bool_opContext
        elif (name == "Expr_bool_opContext"):
            expr1 = self.createREGfrom(ctx.reg_expr(0))
            expr2 = self.createREGfrom(ctx.reg_expr(1))
            return RegOp(RegType.OPERATION, str(ctx.BOOL_OP()), expr1, expr2, None, None)
        #negContext
        elif (name == "Expr_negContext"):
            expr1 = self.createREGfrom(ctx.reg_expr())
            return RegOp(RegType.OPERATION, "!", expr1, None, None, None)
        #atomeContext
        elif (name == "Expr_atomeContext"):
            id = str(ctx.ID())
            if not self.varBlock.getVarWithId(id):
                self.newErrorToPrint(self.getLineNumber(ctx) + " REG block : var \"" + id + "\" used in declaration is not declared.")
            else:
                var = self.varBlock.getVarWithId(id)
                num = int(str(ctx.NUM()))
                if num > var.getLevelBound() or num < 0: #ajouter LevelMin to variable object
                    self.newErrorToPrint(self.getLineNumber(ctx) + " value " + str(num) + " is out of bounds of variable " + id)
                return RegOp(RegType.ATOME, None, None, None, var, num)
        #mux_nameContext
        elif (name == "Expr_mux_nameContext"):
            id = str(ctx.ID())
            regulation = self.regBlock.getRegWithId(id)
            if regulation != None:
                op = regulation.getFormulaTree()
                if op.getRegType() == RegType.ATOME:
                    return RegOp(RegType.ATOME, None, None, None, op.getVar(), op.getThreshold())
                else:
                    return RegOp(op.getRegType(), op.getOperator(), op.getExpr1(), op.getExpr2(), None, None)
            else:
                self.newErrorToPrint(self.getLineNumber(ctx) + " REG block : multiplex SMBname \"" + id + "\" used in declaration has not been declared previously.")
        else:
            self.newErrorToPrint(self.getLineNumber(ctx) + " Unknown REG expression type")
    
        return None



    # *** Hoare Visitors ***
    def visitHybrid_hoare_decl(self, ctx:IGParser.Hybrid_hoare_declContext) -> str:
        #if multiple hybrid hoare blocks ...
        return self.visitChildren(ctx)

    def visitHybrid_hoare_pre_decl(self, ctx:IGParser.Hybrid_hoare_declContext) -> str:
        return self.visitChildren(ctx)

    def visitHybrid_hoare_trace_decl(self, ctx: IGParser.Hybrid_hoare_trace_declContext) -> str:
        
        listEP = []
        for ep_i in range(len(ctx.hybrid_hoare_trace())):
            timeDelay = float(str(ctx.hybrid_hoare_trace(ep_i).FLOAT()))
            if not ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide(0).NOKB() and not self.varBlock.existsVar(str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide(0).ID())):
                self.newErrorToPrint(self.getLineNumber(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide()) + " HYBRID HOARE block -> TRACE, slide part, \"" + str(ep_i) +"\" elementary path : variable \"" + str(str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide().ID())) + "\" has not been declared previously.")
            else:
                slides_info = [] # contains the list of slides (None, 1 or multiple) for each elementary path
                if not ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide(0).NOKB():
                    for i in range(len(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide())):
                        variable=self.getVarBlock().getVarWithId(str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide(i).ID()))
                        slides_info.append((str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide(i).SLIDE()) if ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide(i).SLIDE() else str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide(i).NOSLIDE()), str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide(i).OPER()) if ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_slide(i).OPER() else "", variable))
                else:
                    slides_info.append((None, None, None))
            if not ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_dpa().NOKB() and not self.varBlock.existsVar(str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_dpa().ID())):
                self.newErrorToPrint(self.getLineNumber(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_dpa(0)) + " HYBRID HOARE block -> TRACE, dpa part, \"" + str(ep_i) +"\" elementary path  : variable \"" + str(str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_dpa().ID())) + "\" has not been declared previously.")
            else:
                if not ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_dpa().NOKB():
                    variableD=self.getVarBlock().getVarWithId(str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_dpa().ID()))
                    topBottom = str(ctx.hybrid_hoare_trace(ep_i).hybrid_hoare_dpa().OPER())
                else:
                    variableD = None
                    topBottom = None

            listEP.append(ElementaryPath(timeDelay, slides_info, (variableD, topBottom)))
        
        self.hybridHoareBlock.setTrace(listEP)
        return self.visitChildren(ctx)

    def visitHybrid_hoare_post_decl(self, ctx:IGParser.Hybrid_hoare_post_declContext) -> str:
        
        #TODO : if the entities are not in the right order -> user variable id (not idname)
        sizeDiscreteCondition = len(ctx.discrete_condition())
        sizeHybridCondition = len(ctx.hybrid_condition())

        if sizeDiscreteCondition > 1:
            seenVariables = []
            for i in range(len(ctx.discrete_condition())):
                if not self.varBlock.existsVar(str(ctx.discrete_condition(i).ID())):
                    self.newErrorToPrint(self.getLineNumber(ctx.discrete_condition(i)) + " HYBRID HOARE block -> POST : variable \"" + str(ctx.discrete_condition(i).ID()) + "\" has not been declared previously.")
                elif int(str(ctx.discrete_condition(i).NUM())) > self.varBlock.getVarWithId(str(ctx.discrete_condition(i).ID())).getLevelBound():
                    self.newErrorToPrint(self.getLineNumber(ctx.discrete_condition(i)) + " HYBRID HOARE block -> POST : value \"" +  str(ctx.discrete_condition(i).NUM()) + "\" is out of bounds of variable " + str(ctx.discrete_condition(i).ID()))
                
                #could be great to have the column number where the same entitiy has been seen
                if str(ctx.discrete_condition(i).ID()) in seenVariables:
                    self.newErrorToPrint(self.getLineNumber(ctx.discrete_condition(i)) + " HYBRID HOARE block -> POST : variable \"" + str(ctx.discrete_condition(i).ID()) + "\" has already been declared \"" + str(seenVariables.count(str(ctx.discrete_condition(i).ID()))+1) +  "\" times in the discrete postcondition.")
                else:
                    seenVariables.append(str(ctx.discrete_condition(i).ID()))

        if sizeHybridCondition > 1:
            seenVariables=[]
            
            for i in range(len(ctx.hybrid_condition())):
                if not self.varBlock.existsVar(str(ctx.hybrid_condition(i).ID())):
                    self.newErrorToPrint(self.getLineNumber(ctx.hybrid_condition(i)) + " HYBRID HOARE block -> POST : variable \"" + str(ctx.hybrid_condition(i).ID()) + "\" has not been declared previously.")
                elif float(str(ctx.hybrid_condition(i).FLOAT())) > simulator.constants.FRACTIONAL_PART_TOP or float(str(ctx.hybrid_condition(i).FLOAT())) < simulator.constants.FRACTIONAL_PART_BOTTOM:
                    self.newErrorToPrint(self.getLineNumber(ctx.hybrid_condition(i)) + " HYBRID HOARE block -> POST : value \"" +  str(ctx.hybrid_condition(i).FLOAT()) + "\" is out of fractional part bounds : [0.0, 1.0]")
                
                #could be great to have the column number where the same entitiy has been seen
                if str(ctx.hybrid_condition(i).ID()) in seenVariables:
                    self.newErrorToPrint(self.getLineNumber(ctx.hybrid_condition(i)) + " HYBRID HOARE block -> POST : variable \"" + str(ctx.hybrid_condition(i).ID()) + "\" has already been declared \"" + str(seenVariables.count(str(ctx.hybrid_condition(i).ID()))+1) +  "\" times in the fractional postcondition.")
                else:
                    seenVariables.append(str(ctx.hybrid_condition(i).ID()))

        nb_entities = max(sizeDiscreteCondition, sizeHybridCondition)
        #one is not NOKB so nb_entities is the number of entities
        if nb_entities > 1:
            discreteState = [int(str(ctx.discrete_condition(i).NUM())) if i < sizeDiscreteCondition and not ctx.discrete_condition(i).NOKB() else 0 for i in range(nb_entities)]
            fractionalPart = [float(str(ctx.hybrid_condition(i).FLOAT())) if i < sizeHybridCondition and not ctx.hybrid_condition(i).NOKB() else 0.0 for i in range(nb_entities)]
            postHybridState = HybridState(discreteState, fractionalPart)
        #both are not NOKB : we need varBlock to have the number of entities
        else:
            postHybridState = HybridState([0 for i in range(len(self.varBlock.getData()))], [0.0 for i in range(len(self.varBlock.getData()))])
            
        self.hybridHoareBlock.setPostCondition(postHybridState)
        return self.visitChildren(ctx)
 