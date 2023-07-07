from pymoo.core.problem import ElementwiseProblem
# from eval.utils import *
#euclidean
from math import dist
#manhattan
from scipy.spatial import distance #cityblock
from simulator.hybridstate import HybridState
from simulator.simulator import Simulator
import numpy as np
import time as timer
from functions.functions import tracker



class hGRNProblem(ElementwiseProblem):
    """
    hGRNroblem is an ElementwiseProblem because the _evaluate method needs to be called for each solution.
    """
    def __init__(self, n_var, n_obj, n_constr, xl, xu, simulation:Simulator, BK:list, idxsTabOfCelsToOpt:list[int], criteria:int, typeFitness:str, **kwargs):
        super().__init__(n_var= n_var,
                         n_obj = n_obj,
                         n_constr = n_constr,
                         xl = xl,
                         xu = xu,
                        **kwargs)
        self.tracker = None
        self.simulation = simulation
        self.BK = BK
        self.idxsTabOfCelsToOpt= idxsTabOfCelsToOpt
        self.criteria = criteria
        self.typeFitness = typeFitness
        self.pBname="hGRNProblem_"+str(self.criteria)+"criteria_"+self.typeFitness

    def initiate_tracker(self, complement):
        self.tracker = tracker('bioinsp_' + complement, True)


    def _evaluate(self, solution,  out, *args, **kwargs):
        """
        The evaluation function of the distance bewteen the simulated biological trace and the actual biological knowledge.
        """

        startWallTimeEvalInd = timer.time()
        startProcTimeEvalInd = timer.process_time()

        #Biological knowledge with comparable information
        BK_time, BK_gliss, BK_gliss_entity, BK_gliss_top_bottom, BK_disc_trans, BK_disc_trans_var, BK_dist_partFrac = self.BK


        #1- Reconstruct the solution here
        if self.idxsTabOfCelsToOpt != None:
            allCels = self.simulation.getAllCelerities()
            a=0
            for idxCel in range(len(allCels)):
                if idxCel in self.idxsTabOfCelsToOpt:
                    allCels[idxCel].setValue(solution[a])
                    a+=1
        else:
            self.simulation.setCeleritiesValue(solution)
        #2 - Launch the simulation and reset trace
        self.simulation.reset()
        startWallTimeSimulInd = timer.time()
        startProcTimeSimulInd = timer.process_time()
        #self.simulation.simulateDispiteBlockagesAndBadTransitions(len(BK_disc_trans), 48., 0., -1, self.simulation.getVariables(), self.simulation.getInitialHybridState(), self.simulation.getAllCelerities())
        self.simulation.simulation()
        endProcTimeSimulInd = timer.process_time()
        endWallTimeSimulInd = timer.time()
        trace = self.simulation.getTrace()
        # for path in trace:
        #    print(path[0], " ", path[1])
        #3 - The core of the evaluation function
        ## Three continuous fitness values
        ### the euclidian distance in time : dist(actual, knowledge)
        time_distance = 0
        ### if the entity has not slid when it should have or inversely, it is penalized by the position it sould have gone to
        slide_distance = 0
        ### the manhattan distance in position : dist(actual, knowledge)
        discrete_distance = 2 * self.simulation.getBadTransitionsCount()
        ## blockages distance : number of blockages happened during the simulation (must be minimized and its maximum is the length of the hybrid Hoare triplet)
        blockages_distance = self.simulation.getBlockagesCount()

        ## Counter : +1 when an exit point is simulated
        cpt = 0
        #saveTime table : saves the last exit point time simulated, we want to penalize the time duration in one step
        saveTime = [0.]
        #listFirstSlidingPoint : saves information about the *last* first sliding point encountered : (time, hybridState)
        lastFirstSlidingPoint = ()
        #Main loop: begin at index 1 because first info is about initial hybrid state which is known for the moment and last one is initial hybrid point so the one before the last is an exit point
        for i in range(1, len(trace)-1):
            #for debug
            #we only need to penalize the first sliding point : there are maximum n-1 slides
            #get the first sliding point if any
            _, prevHybridState = trace[i-1]
            time, hybridState = trace[i]
            nextTime, nextHybridState = trace[i+1]

            #the last one saved during the simulation is considered as an exit point (because it must be it)
            if i == len(trace)-2 or hybridState.isAnExitPoint(nextHybridState):

                ### TIME ###
                time_distance += dist([time - saveTime[cpt]], [BK_time[cpt]])

                #### SLIDE ###
                #Check if there are any information given by BK
                if BK_gliss[cpt] != None:
                    #It could have multiple slides !
                    for n in range(len(BK_gliss[cpt])):
                        gliss = BK_gliss[cpt][n]
                        eGliss = BK_gliss_entity[cpt][n]
                        # Returns True if there is a problem between knowledge and simulation
                        #if (prevHybridState.getDiscreteState() == hybridState.getDiscreteState()) ^ gliss:
                        if (lastFirstSlidingPoint != ()) ^ gliss:
                            #a) it should have slid
                            if gliss:
                                slide_distance += abs(hybridState.getFractionalPart()[eGliss.getId()] - BK_dist_partFrac[eGliss.getId()][cpt])

                            #b) it should not have slid
                            elif not gliss:
                                #Please note that if there are multiple (m) sliding points it will be calculated m times
                                slide_distance += distance.cityblock(np.array([lastFirstSlidingPoint[1].getFractionalPart()[BK_disc_trans_var[cpt].getId()]]), np.array([BK_dist_partFrac[BK_disc_trans_var[cpt].getId()][cpt]]))
                        #There is no apaprent sliding problem but an entity could slide on the wrong face !
                        else:
                            if gliss:
                                bGliss = BK_gliss_top_bottom[cpt][n]
                                #penalize if slide top
                                if bGliss == "top":
                                    slide_distance += abs(hybridState.getFractionalPart()[eGliss.getId()] - 1.0)
                                #penalize if slide bottom
                                elif bGliss == "bottom":
                                    slide_distance += abs(hybridState.getFractionalPart()[eGliss.getId()] - 0.0)
                # next exit point
                cpt+=1
                saveTime.append(time)
            else:
                #if the actual hybrid state is an entry HS then it is not a sliding point if there are one it will be the next
                if prevHybridState.isAnExitPoint(hybridState): #this ùeans that this is an entry HS
                    # if i+1 == len(trace)-1 or nextHybridState.isAnExitPoint(trace[i+2][1]):
                    #     lastFirstSlidingPoint = (time, hybridState)
                    # else:
                    lastFirstSlidingPoint = ()
                else:
                    if lastFirstSlidingPoint == ():
                        lastFirstSlidingPoint = (time, hybridState)
                        #lastFirstSlidingPoint = (nextTime, nextHybridState)

        # firstHS = trace[0][1]
        # finalHS = trace[len(trace)-1][1]
        # dFinalHS = sum([abs(finalHS.getFractionalPart()[i] - firstHS.getFractionalPart()[i]) for i in range(len(finalHS.getFractionalPart()))])



        if self.criteria == 4:
            #SUM (Note: same as sum with 3 criteria)
            if(self.typeFitness == "sum"):
                global_fitness = time_distance + slide_distance + discrete_distance + blockages_distance #+ dFinalHS
            #PRODUCT
            elif(self.typeFitness == "product"):
                global_fitness = (1+time_distance) * (1+slide_distance) * (1+discrete_distance) * (1+blockages_distance) - 1
        elif self.criteria == 3:
            #SUM (3 == 4)
            if(self.typeFitness == "sum"):
                global_fitness = time_distance + slide_distance + (discrete_distance + blockages_distance) #+ dFinalHS
            #PRODUCT
            elif(self.typeFitness == "product"):
                global_fitness = (1+time_distance) * (1+slide_distance) * (1+discrete_distance+blockages_distance) - 1
        else:
            print("3 or 4 criteria only for the moment")

        # print("Single obj fitness :", global_fitness)
        # print(time_distance)
        # print(slide_distance)
        # print("___________________________________________\n")

        self.tracker.track_celerities(global_fitness, self.simulation.getAllCelerities())
            
        #print(global_fitness)

        endProcTimeEvalInd = timer.process_time()
        endWallTimeEvalInd = timer.time()

        elapsedProcTimeSimulInd = endProcTimeSimulInd - startProcTimeSimulInd
        elapsedWallTimeSimulInd = endWallTimeSimulInd - startWallTimeSimulInd
        elapsedProcTimeEvalInd = endProcTimeEvalInd - startProcTimeEvalInd
        elapsedWallTimeEvalInd = endWallTimeEvalInd - startWallTimeEvalInd

        #out["F"] = np.array([global_fitness]).astype(np.float64)
        out["F"] = [global_fitness]

        out["fitnessTime"] = [time_distance]
        out["fitnessSlide"] = [slide_distance]
        out["fitnessDiscrete"] = [discrete_distance]
        out["fitnessBlockages"] = [blockages_distance]
        out["fitnessDiscreteAndBlockages"] = [discrete_distance + blockages_distance]
        out["fitnessCycleHS"] = [0.]#[dFinalHS]

        out["procTimeSimulInd"] = np.array(elapsedProcTimeSimulInd)
        out["wallTimeSimulInd"] = np.array(elapsedWallTimeSimulInd)
        out["procTimeEvalInd"] = np.array(elapsedProcTimeEvalInd)
        out["wallTimeEvalInd"] = np.array(elapsedWallTimeEvalInd)
