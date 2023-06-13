from math import dist
from typing import Tuple, Any

from scipy.spatial import distance
from simulator.simulator import Simulator
import numpy as np


def f_objective(X, simulation: Simulator, BK: list, criteria: int = 3, typeFitness: str = "sum") -> tuple[
    int | Any, int, int, int | Any, Any, int | Any]:
    """
    The evaluation/fitness function calculated as the distance between the simulated trace and the actual biological knowledge.
    """

    # Biological knowledge with comparable information
    BK_time, BK_gliss, BK_gliss_entity, BK_gliss_top_bottom, BK_disc_trans, BK_disc_trans_var, BK_dist_partFrac = BK

    # 1- Set the solution of celerities
    simulation.setCeleritiesValue(X)
    # 2 - Launch the simulation and reset trace
    simulation.simulation()
    trace = simulation.getTrace()
    # 3 - The core of the evaluation function
    ## Three continuous fitness values
    ### the euclidian distance in time : dist(actual, knowledge)
    time_distance = 0
    ### if the entity has not slid when it should have or inversely, it is penalized by the position it sould have gone to
    slide_distance = 0
    ### the manhattan distance in position : dist(actual, knowledge) NOW extrapolated from simulation
    discrete_distance = 2 * simulation.getBadTransitionsCount()
    ## blockages distance : number of blockages happened during the simulation (must be minimized : longueur du triplet max)
    blockages_distance = simulation.getBlockagesCount()

    ## Counter : +1 when an exit point is detected
    cpt = 0
    # saveTime saves the last exit point time simulated
    saveTime = [0.]
    # listFirstSlidingPoint : saves information about the *last* first sliding point encountered : (time, hybridState)
    lastFirstSlidingPoint = ()

    # Main loop: iterate over the simulated trace saved points
    for i in range(1, len(trace) - 2):
        prevTime, prevHybridState = trace[i - 1]
        time, hybridState = trace[i]
        nextTime, nextHybridState = trace[i + 1]
        # the last one is an exit point, for sure
        if i == len(trace) - 2 or hybridState.isAnExitPoint(nextHybridState):
            ##### TIME
            # time_distance += dist([time], [BK_time[cpt]])

            try:
                time_distance += dist([time - saveTime[cpt]], [BK_time[cpt]])
            except IndexError:
                print("cpt", cpt)
                print("saveTime", saveTime)
                print("BK_time", BK_time)

            #### SLIDE ###
            # Check if there are any information given by BK
            if BK_gliss[cpt] != None:
                # It could have multiple slides !
                for n in range(len(BK_gliss[cpt])):
                    gliss = BK_gliss[cpt][n]
                    eGliss = BK_gliss_entity[cpt][n]
                    # Returns True if there is a problem between knowledge and simulation 
                    if (lastFirstSlidingPoint != ()) ^ gliss:
                        # a) it should have slid
                        if gliss:
                            slide_distance += abs(
                                hybridState.getFractionalPart()[eGliss.getId()] - BK_dist_partFrac[eGliss.getId()][cpt])

                        # b) it should not have slid
                        elif not gliss:
                            # Please note that if there are multiple (m) sliding points it will be calculated m times
                            slide_distance += distance.cityblock(
                                np.array(
                                    [lastFirstSlidingPoint[1].getFractionalPart()[BK_disc_trans_var[cpt].getId()]]),
                                np.array([BK_dist_partFrac[BK_disc_trans_var[cpt].getId()][cpt]])
                            )
                    # There is no apaprent sliding problem but an entity could slide on the wrong face !
                    else:
                        if gliss:
                            bGliss = BK_gliss_top_bottom[cpt][n]
                            # penalize if slide top
                            if bGliss == "top":
                                slide_distance += abs(hybridState.getFractionalPart()[eGliss.getId()] - 1.0)
                            # penalize if slide bottom
                            elif bGliss == "bottom":
                                slide_distance += abs(hybridState.getFractionalPart()[eGliss.getId()] - 0.0)
            # next exit point
            cpt += 1
            saveTime.append(time)
        else:
            # if the actual hybrid state is an entry HS then it is not a sliding point if there are one it will be the next
            if prevHybridState.isAnExitPoint(hybridState):  # this means that this is an entry HS
                lastFirstSlidingPoint = ()
            else:
                # first sliding point
                if lastFirstSlidingPoint == ():
                    lastFirstSlidingPoint = (time, hybridState)
                # n-th sliding point

    if criteria == 4:
        # SUM (Note: same as sum with 3 criteria)
        if (typeFitness == "sum"):
            global_fitness = time_distance + slide_distance + discrete_distance + blockages_distance
        # PRODUCT
        elif (typeFitness == "product"):
            global_fitness = (1 + time_distance) * (1 + slide_distance) * (1 + discrete_distance) * (
                        1 + blockages_distance) - 1
    elif criteria == 3:
        # SUM (3 == 4)
        if (typeFitness == "sum"):
            global_fitness = time_distance + slide_distance + (discrete_distance + blockages_distance)
        # PRODUCT
        elif (typeFitness == "product"):
            global_fitness = (1 + time_distance) * (1 + slide_distance) * (
                        1 + discrete_distance + blockages_distance) - 1
    else:
        raise ("3 or 4 criteria only")

    print(
        "distance by criteria - time: " + str(time_distance) + "; slide: " + str(slide_distance) + "; disrete: " + str(
            discrete_distance) + "; blocakges: " + str(blockages_distance))

    return global_fitness, time_distance, slide_distance, discrete_distance, blockages_distance, (
                discrete_distance + blockages_distance)
