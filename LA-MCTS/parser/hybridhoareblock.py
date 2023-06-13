from simulator.constants import EPSILON
from simulator.hybridstate import HybridState
from parser.elementarypath import ElementaryPath

class HybridHoareBlock:

    def __init__(self) -> None:
        self.cyclic = False
        self.preCondition = HybridState([], [])
        self.trace = [] #list of elementarypath
        self.postCondition = HybridState([], [])

    def setCyclic(self) -> None:
        self.cyclic = True

    def isCyclic(self) -> bool:
        return self.cyclic

    def getPreCondition(self) -> HybridState:
        return self.preCondition

    def setPreCondition(self, preState:HybridState) -> None:
        self.preCondition = preState

    def getPostCondition(self) -> HybridState:
        return self.postCondition
    
    def getTrace(self) -> list[ElementaryPath]:
        return self.trace

    def setPostCondition(self, postState:HybridState) -> None:
        self.postCondition = postState
    
    def setTrace(self, newTrace:list[ElementaryPath]) -> None:
        self.trace = newTrace


    def generateComparatorsListForFitnessEval(self):
        """
        Different lists are provided : each one of them is used to compare the simulated trace to the knowledge.
        Outputs the simulated knowledge for comparisions (from hoare triple to convenient form)
        """
        #Time for continuous transitions
        BK_time = []
        #Slide in assertion couple : does it slide or not, which entity and top or bottom ?
        BK_gliss = []
        BK_gliss_entity = []
        BK_gliss_top_bottom = []
        #Discrete transition
        BK_disc_trans = []
        BK_disc_trans_var = []
        #Part frac but it needs full information at begin which might not be the case...
        BK_dist_partFrac = []

        for i in range(len(self.getTrace())):
            path = self.getTrace()[i]
            #List of times sumed up
            # if i > 0:
            #     addition = BK_time[i-1] 
            # else:
            #     addition = 0
            BK_time.append(path.getTransitionDelay())# + addition)

            #Slide
            gliss = []
            gliss_entity = []
            gliss_top_bottom = []
            for aE in path.getAssertionElement():
                slideOrNotOrNone, topBottomOrNiente, varAss = aE
                if slideOrNotOrNone == "slide":
                    gliss.append(True)
                elif slideOrNotOrNone == "noslide":
                    gliss.append(False)
                else:
                    gliss.append(None)
                gliss_entity.append(varAss)
                if topBottomOrNiente == "+":
                    gliss_top_bottom.append("top")
                elif topBottomOrNiente == "-":
                    gliss_top_bottom.append("bottom")
                else:
                    gliss_top_bottom.append(None) 
            if len(gliss) > 1:
                BK_gliss.append(gliss)
                BK_gliss_entity.append(gliss_entity)
                BK_gliss_top_bottom.append(gliss_top_bottom)
            else:
                BK_gliss.append([gliss[0]] if gliss[0] != None else None)
                BK_gliss_entity.append([gliss_entity[0]] if gliss_entity[0] != None else None)
                BK_gliss_top_bottom.append([gliss_top_bottom[0]] if gliss_top_bottom[0] != None else None)

            #Discrete Trans
            varDpa, plusMinus = path.getAtomDiscretePath()
            # CHECK THIS : if not (var == None): BUT HOW TO CALCULATE NEXT STATE ?
            if i > 0:
                newDiscreteState = BK_disc_trans[i-1].copy()
            else: 
                newDiscreteState = self.getPreCondition().getDiscreteState().copy()
            if plusMinus == "+":
                newDiscreteState[varDpa.getId()] += 1
            else:
                newDiscreteState[varDpa.getId()] -=1
            assert newDiscreteState[varDpa.getId()] >= 0, "-1 as a discrete state is not possible, please double check the hybrid hoare trace."
            BK_disc_trans.append(newDiscreteState)
            BK_disc_trans_var.append(varDpa)

            #PartFrac info 
            partFrac = [[0., 1.] for i  in range(len(self.getPreCondition().getDiscreteState()))]
            for aE in path.getAssertionElement():
                slideOrNotOrNone, topBottomOrNiente, varAss = aE
                if slideOrNotOrNone == "slide":
                    if topBottomOrNiente == "+":
                        partFrac[varAss.getId()] = 1.
                    elif topBottomOrNiente == "-":
                        partFrac[varAss.getId()] = 0.
                elif slideOrNotOrNone == "noslide":
                    if topBottomOrNiente == "+":
                        partFrac[varAss.getId()] = [0., 1.-EPSILON]
                    elif topBottomOrNiente == "-":
                        partFrac[varAss.getId()] = [0.+EPSILON, 1.]
            
            if plusMinus == "+":
                partFrac[varDpa.getId()] = 1.
            elif plusMinus == "-":
                partFrac[varDpa.getId()] = 0.
            BK_dist_partFrac.append(partFrac)

            #Transform the last list in sublist per variable
            BK_part_frac_per_var = [[inf[j] for inf in BK_dist_partFrac] for j in range(len(BK_dist_partFrac[0]))]


        return (BK_time, BK_gliss, BK_gliss_entity, BK_gliss_top_bottom, BK_disc_trans, BK_disc_trans_var, BK_part_frac_per_var)