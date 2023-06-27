# simulator imports
from simulator.utils import *
from simulator.constants import *
from simulator.simulator import Simulator

# SOEA
from eval.hGRNProblem import hGRNProblem
from pymoo.core.callback import Callback

# PyMOO imports
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.ga_niching import NicheGA
from pymoo.algorithms.soo.nonconvex.de import DE
from pymoo.algorithms.soo.nonconvex.cmaes import CMAES
from pymoo.algorithms.soo.nonconvex.pso import PSO
from algorithms.randomsearch import optimize, population_optimizer
from pymoo.core.evaluator import Evaluator
from pymoo.factory import get_termination
from pymoo.optimize import minimize
from pymoo.core.population import Population

# utils and os
import utils.utils as utils, os, time, math
# fix random with seed
from random import seed
import numpy as np
from datetime import datetime
from shutil import copyfile
import csv

# Visualisation
import matplotlib.pyplot as plt

# pymoo threads
from pymoo.core.problem import starmap_parallelized_eval
# processes
import multiprocessing


class MyCallback(Callback):
    """
     Callback class can be used to receive a notification of the algorithm object each generation
    """

    def __init__(self) -> None:
        super().__init__()

        # number of evaluations
        self.data['n_evals'] = []
        # opt (a Population object), which contains the current optimum
        self.data['opt'] = []

        self.data['gen_std'] = []

        # generation counter
        self.data["gen"] = []

        self.data["best"] = []
        self.data["worst"] = []
        self.data["avg"] = []
        self.data["std"] = []

        self.data["individuals"] = []
        self.data["fitness"] = []

        self.data['fitnessTime'] = []
        self.data['fitnessSlide'] = []
        self.data['fitnessBlockages'] = []
        self.data['fitnessDiscrete'] = []
        self.data['fitnessCycleHS'] = []

        self.data['wallTimeSimulInd'] = []
        self.data['wallTimeSimulIndMin'] = []
        self.data['wallTimeSimulIndMax'] = []
        self.data['wallTimeSimulIndAvg'] = []
        self.data['wallTimeSimulIndStd'] = []
        self.data['procTimeSimulInd'] = []
        self.data['procTimeSimulIndMin'] = []
        self.data['procTimeSimulIndMax'] = []
        self.data['procTimeSimulIndAvg'] = []
        self.data['procTimeSimulIndStd'] = []
        self.data['wallTimeEvalInd'] = []
        self.data['wallTimeEvalIndMin'] = []
        self.data['wallTimeEvalIndMax'] = []
        self.data['wallTimeEvalIndAvg'] = []
        self.data['wallTimeEvalIndStd'] = []
        self.data['procTimeEvalInd'] = []
        self.data['procTimeEvalIndMin'] = []
        self.data['procTimeEvalIndMax'] = []
        self.data['procTimeEvalIndAvg'] = []
        self.data['procTimeEvalIndStd'] = []

    def notify(self, algorithm):
        # algorithm.off => non-elitist, algorithm.pop => elitist

        # Monotonic convergence analysis
        self.data['n_evals'].append(algorithm.evaluator.n_eval)
        self.data['opt'].append(algorithm.opt[0].F)

        # Standard deviation of population
        self.data['gen_std'].append(np.std(algorithm.pop.get("X")))

        # Populations infos
        self.data["gen"].append(algorithm.n_gen)

        self.data["best"].append(algorithm.pop.get("F").min())
        self.data["worst"].append(algorithm.pop.get("F").max())
        self.data["avg"].append(algorithm.pop.get("F").mean())
        self.data["std"].append(np.std(algorithm.pop.get("F")))

        self.data["individuals"].append(algorithm.pop.get("X"))  # [::-1])
        self.data["fitness"].append(algorithm.pop.get("F"))  # [::-1])
        # self.data["fitness"].append(algorithm.pop.get("F"))#[::-1])
        # print(self.data['individuals'][-1][-10:])

        self.data['fitnessTime'].append(algorithm.pop.get('fitnessTime'))  # [::-1])
        self.data['fitnessSlide'].append(algorithm.pop.get('fitnessSlide'))  # [::-1])
        self.data['fitnessBlockages'].append(algorithm.pop.get('fitnessBlockages'))  # [::-1])
        self.data['fitnessDiscrete'].append(algorithm.pop.get('fitnessDiscrete'))  # [::-1])
        self.data['fitnessCycleHS'].append(algorithm.pop.get('fitnessCycleHS'))

        self.data['wallTimeSimulInd'].append(algorithm.pop.get("wallTimeSimulInd"))
        self.data['wallTimeSimulIndMin'].append(algorithm.pop.get("wallTimeSimulInd").min())
        self.data['wallTimeSimulIndMax'].append(algorithm.pop.get("wallTimeSimulInd").max())
        self.data['wallTimeSimulIndAvg'].append(algorithm.pop.get("wallTimeSimulInd").mean())
        self.data['wallTimeSimulIndStd'].append(np.std(algorithm.pop.get("wallTimeSimulInd")))

        self.data['procTimeSimulInd'].append(algorithm.pop.get("procTimeSimulInd"))
        self.data['procTimeSimulIndMin'].append(algorithm.pop.get("procTimeSimulInd").min())
        self.data['procTimeSimulIndMax'].append(algorithm.pop.get("procTimeSimulInd").max())
        self.data['procTimeSimulIndAvg'].append(algorithm.pop.get("procTimeSimulInd").mean())
        self.data['procTimeSimulIndStd'].append(np.std(algorithm.pop.get("procTimeSimulInd")))

        self.data['wallTimeEvalInd'].append(algorithm.pop.get("wallTimeEvalInd"))
        self.data['wallTimeEvalIndMin'].append(algorithm.pop.get("wallTimeEvalInd").min())
        self.data['wallTimeEvalIndMax'].append(algorithm.pop.get("wallTimeEvalInd").max())
        self.data['wallTimeEvalIndAvg'].append(algorithm.pop.get("wallTimeEvalInd").mean())
        self.data['wallTimeEvalIndStd'].append(np.std(algorithm.pop.get("wallTimeEvalInd")))

        self.data['procTimeEvalInd'].append(algorithm.pop.get("procTimeEvalInd"))
        self.data['procTimeEvalIndMin'].append(algorithm.pop.get("procTimeEvalInd").min())
        self.data['procTimeEvalIndMax'].append(algorithm.pop.get("procTimeEvalInd").max())
        self.data['procTimeEvalIndAvg'].append(algorithm.pop.get("procTimeEvalInd").mean())
        self.data['procTimeEvalIndStd'].append(np.std(algorithm.pop.get("procTimeEvalInd")))


# PATH = "/home/.../.../"

if __name__ == '__main__':

    # Start the execution wall time clock for the experiment
    startWallTimeExperiment = datetime.now()

    ### A) Set up the experiment based on the information gathered ###

    # 1. Read the config file that contains all the experiment settings
    config = utils.import_settings_configuration(config_file='exp_settings.ini')

    # 2. Parse the SMB file that contains specifications about the biological interaction graph
    variables, _, initialHybridState, _, BK = utils.parse(config['smb'], False)

    # 3. Set up the simulator
    simulator = Simulator(variables, initialHybridState, BK)
    allCels = simulator.getAllCelerities()
    nbOfVariables = len(allCels)
    print("Number of celerities in the simulator:", nbOfVariables)
    idxsTabOfCelsToOpt = None

    # 4. only optimize variables that are needed for the global trajectory
    # celsToOpt, celRanges = generateCeleritiesToOptimizeAndRanges(BK, variables)
    celsToOpt = generateCeleritiesToOptimize(BK[4], variables)
    # print(celRanges)
    nbOfVariables = len(celsToOpt)
    print("Number of celerities to optimize:", nbOfVariables)
    # assert nbOfVariables == len(celRanges), "Problem between ranges length and nbOfVariables to optimize"
    idxsTabOfCelsToOpt = utils.getIdxsOfCelToOptimize(allCels, celsToOpt)
    print("Indexes of celerities that are useful:", idxsTabOfCelsToOpt)
    assert len(idxsTabOfCelsToOpt) == nbOfVariables, "Pb here..."
    for idxCels in range(len(allCels)):
        if (idxCels in idxsTabOfCelsToOpt):
            print(allCels[idxCels])

            ### B) Create the environment to save the data ####

    # 1. Create the directory root at the desired path to save all the data later on
    rootSavePath = config['results_dir_name'] + "/" + config['experiment_dir_name'] + "/"
    utils.create_directory(rootSavePath)

    # 2. Initialize the random seeds and save them in a file
    # seeds = [randrange(1, 1000000) for i in range(config['n_test'])]
    # seeds = utils.parse_seeds("seeds.txt", "res_ea_100_OFF/sum/")
    # print(len(seeds))
    # seeds = [i for i in range(1, config['n_test']+1)] #could be config['seed_min'], config['seed_max']
    seeds = [utils.parse_seeds("seeds.txt", "../results/res_ea_100_OFF/sum/")[i] for i in
             range(config['from'] - 1, config['n_test'])]
    utils.save_seeds(rootSavePath, seeds, config['debug'])

    # 3. Save the experiment parameters file
    copyfile(src='exp_settings.ini',
             dst=os.path.join(config['results_dir_name'], config['experiment_dir_name'], 'settings.ini'))
    if config['debug']:
        print("> Settings file saved\n")

    ### C) Set up the framework pymoo for the experiment ###

    # 1. Get the multiprocessing pool initialized for speeding up the evaluation process (from PyMoo)
    n_proccess = 16
    pool = multiprocessing.Pool(n_proccess)
    # WAS HERE
    problem = hGRNProblem(nbOfVariables, config['objectives'], config['constraints'],
                          [float(-config['celerities_range']) for i in range(nbOfVariables)],
                          [float(config['celerities_range']) for i in range(nbOfVariables)], simulator, BK,
                          idxsTabOfCelsToOpt, config['criteria'], config['type'], runner=pool.starmap,
                          func_eval=starmap_parallelized_eval)
    # [float(-config['celerities_range']) for i in range(nbOfVariables)]
    # [float(config['celerities_range']) for i in range(nbOfVariables)]
    # 3. Set the termination criterion
    termination = get_termination("n_eval", config['evaluations'])
    # termination = get_termination("n_gen", config['evaluations']//config['population_size']+1)

    ### D) Launch the framework ###

    # 1. The first loop iterates over the different algorithms launched
    for algorithm_name in config['algorithm']:
        if config['debug']:
            print('Algo : ', algorithm_name, '\n')

        # 2. Create the sub-directory that takes the algorithm as name to save the different runs
        utils.create_directory(algorithm_name, rootSavePath)
        subRootSavePath = rootSavePath + algorithm_name + '/'

        # 3. The second loop iterates over the number of runs decided
        for i in range(len(seeds)):
            # 4. Start the wall time clock to evaluate the performances of each run
            startWallTimeRun = datetime.now()

            # 5. Initialize the variable seed and set it up in the numpy random generator
            numSeed = seeds[i]
            if config['debug']:
                print('Seed num : ', numSeed, '\n')
            np.random.seed(numSeed)

            # 6. Create a sub-sub-directory for the seed (it's where every information relative to the run is saved)
            if config['n_test'] > 1:
                utils.create_directory(str((config['from'] + i - 1) + 1), subRootSavePath)
                savePath = subRootSavePath + str((config['from'] + i - 1) + 1) + "/"
            else:
                savePath = subRootSavePath
            if config['debug']:
                print('Path where data of the run is saved: ', savePath)

            # START CP
            # xl, xu = [], []
            # exactCelsValues=[]
            # #NEW. Launch the solver and calculate the bounds given the CSP output
            # utils.launch_solver(config['smb'], "res_path_"+config['smb']+"_GA", numSeed, 1, 24)

            # if config['smb'] == "test" or config['smb'] == "circadian_clock":
            #     copyfile(src=PATH+"res_path_"+config['smb']+"_GA/cel_file", dst=os.path.join(savePath, 'cel_file'))
            #     #with open(PATH+"res_path_"+config['smb']+"/cel_file") as f:
            #     with open(savePath+'cel_file') as f:
            #         lines = [line.rstrip() for line in f]
            #     varNames, minBounds, maxBounds = utils.utils.split_bounds(lines, "=", False)

            # else:
            #     copyfile(src=PATH+"res_path_"+config['smb']+"_GA/temp", dst=os.path.join(savePath, 'cel_file'))
            #     with open(savePath+'cel_file') as f:
            #         lines = [el for line in f for el in line.split( ) if "C_" in el]
            #     lines[0] = lines[0][1:]
            #     varNames, minBounds, maxBounds = utils.utils.split_bounds(lines, ":", False)

            # #print("CHECK 1: ", idxsTabOfCelsToOpt)
            # idxsTabOfCelsToOptForThisRun=idxsTabOfCelsToOpt.copy()
            # #print("CHECK 2: ", idxsTabOfCelsToOptForThisRun)
            # #print("CHECK 3: ", len(allCels))
            # #print("CHECK 4: ", len(simulator.getAllCelerities()))
            # for idxCel in range(len(allCels)):
            #     if (idxCel in idxsTabOfCelsToOpt):
            #         try:
            #             idx=varNames.index(allCels[idxCel].getString())
            #             xl_val=minBounds[idx]
            #             xu_val=maxBounds[idx]
            #             if xl_val == xu_val and len(str(xl_val).rsplit('.')[-1]) < 4:
            #                 simulator.getAllCelerities()[idxCel].setValue(xl_val)
            #                 idxsTabOfCelsToOptForThisRun.remove(idxCel)
            #                 #can be removed but just to check
            #                 exactCelsValues.append((idxCel, xl_val))
            #             else:
            #                 xl.append(math.floor(xl_val*10)/10)
            #                 xu.append(math.ceil(xu_val*10)/10)
            #         except Exception:
            #             raise("Not found...")

            # assert len(xl) == len(xu), "Bounds list must have the same length..."
            # # print(xl)
            # # print(xu)
            # # print("Number of bounds: ", len(xl))
            # # print(exactCelsValues)
            # # print("Number of celerities for which we have the exact value: ", len(exactCelsValues))
            # nbOfVariables=len(idxsTabOfCelsToOptForThisRun)
            # assert nbOfVariables == len(idxsTabOfCelsToOpt) - len(exactCelsValues), "Problem of lengths..."
            # #print("Number of celerities to optimize (useful-CSP): ", nbOfVariables)

            # #2. Set up the optimization problem with the parameters depending on the experiment launched
            # problem = hGRNProblem(nbOfVariables, config['objectives'], config['constraints'], xl, xu, simulator, BK, idxsTabOfCelsToOptForThisRun, config['criteria'], config['type'], runner=pool.starmap, func_eval=starmap_parallelized_eval)
            # X=[]
            # for _ in range(config['population_size']):
            #     ind=[]
            #     for _ in range(problem.n_var):
            #         ind.append(np.random.uniform(xl[len(ind)], xu[len(ind)]))
            #     X.append(ind)
            #### END CP

            # 7. Generate and set up the same initial population for every algorithm
            X = (config['celerities_range'] * 2) * np.random.random_sample((config['population_size'], problem.n_var)) - \
                config['celerities_range']
            # print(len(X))
            # print(X[0])
            # exit()
            utils.save_population(savePath, "init_pop", X, config['debug'])
            utils.save_population_csv(savePath, "init_pop", X, config['debug'])  # .tolist()!
            initialPop = Population.new("X", X)
            Evaluator().eval(problem, initialPop)

            # 8. Decide which algorithm to run
            ### GA ###
            if algorithm_name == 'ga':
                if config['debug']:
                    print("GA")
                algorithm = GA(pop_size=config['population_size'],
                               sampling=initialPop,
                               eliminate_duplicates=True)
            ### GA + NICHING ###
            elif algorithm_name == 'ga_niching':
                if config['debug']:
                    print("GA Niching")
                algorithm = NicheGA(pop_size=config['population_size'],
                                    norm_niche_size=.25,
                                    sampling=initialPop,
                                    eliminate_duplicates=True)
            ### PSO ###
            elif algorithm_name == 'pso':
                if config['debug']:
                    print("PSO")
                algorithm = PSO(pop_size=config['population_size'],
                                sampling=initialPop)
                # sampling=FloatRandomSampling())
            ### Differential Evolution ###
            elif algorithm_name == 'de':
                if config['debug']:
                    print("DE")
                algorithm = DE(pop_size=config['population_size'],
                               sampling=initialPop,
                               # F=0.5,
                               variant="DE/rand/1/bin",  # best
                               CR=0.3,  # 0.5
                               dither="vector",
                               jitter=False)
            ### CMAES ###
            elif algorithm_name == 'cmaes':
                if config['debug']:
                    print("CMAES")
                algorithm = CMAES(popsize=config['population_size'],
                                  x0=initialPop)  # , cmaes_verbose=3)#, tolfun=0, tolfunhist=0, tolx=0, cmaes_verbose=3)#, CMA_elitist=True, eval_initial_x=None)

            # 9. Launch the optimization with callbacks
            res = minimize(problem,
                           algorithm,
                           termination,
                           seed=numSeed,
                           # save_history=True,
                           copy_algorithm=False,
                           callback=MyCallback(),
                           verbose=True)

            # 10. Stop the wall time clock for the run (save it in 17.)
            endWallTimeRun = datetime.now()
            elapsedWallTimeRun = endWallTimeRun - startWallTimeRun

            if config['debug']:
                print('Processes:', res.exec_time)
                print(res.algorithm.callback.data['n_evals'][-1])
            # if res.algorithm.callback.data['n_evals'][-1] != config['evaluations']:
            #     seeds.append(randrange(1, 1000000))
            #     print(len(seeds))

            # 11. Save information about the monotonic convergence
            # MONOTONIC CONVERGENCE
            fieldnames = ['seed', 'n_evals', 'opt']
            if (not (os.path.isfile(subRootSavePath + 'convergence.csv'))):
                with open(subRootSavePath + 'convergence.csv', 'w') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(fieldnames)
                    for i in range(len(res.algorithm.callback.data['n_evals'])):
                        writer.writerow([numSeed, res.algorithm.callback.data['n_evals'][i],
                                         res.algorithm.callback.data['opt'][i][0]])

                if config['debug']:
                    print("> convergence.CSV created")
            else:
                with open(subRootSavePath + 'convergence.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    for i in range(len(res.algorithm.callback.data['n_evals'])):
                        writer.writerow([numSeed, res.algorithm.callback.data['n_evals'][i],
                                         res.algorithm.callback.data['opt'][i][0]])
                if config['debug']:
                    print("> convergence.CSV appended")

                    # POP LEVEL
            fieldnames = ['seed', 'gen', 'nfe', 'individuals', 'fitness', 'fitnessTime', 'fitnessSlide',
                          'fitnessDiscrete', 'fitnessBlockages', 'fitnessCycleHS', 'wallTimeSimul', 'cpuTimeSimul',
                          'wallTimeEval', 'cpuTimeEval']
            if (not (os.path.isfile(subRootSavePath + 'pop_info_level.csv'))):
                with open(subRootSavePath + 'pop_info_level.csv', 'w') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(fieldnames)
                    nfe = 0
                    # for pop in pops
                    for i in range(len(res.algorithm.callback.data['individuals'])):
                        # assert len(set(res.algorithm.callback.data['fitness'][i].flatten())) == len(res.algorithm.callback.data['fitness'][i])
                        # for ind in individuals
                        for x in range(len(res.algorithm.callback.data['individuals'][i])):
                            nfe += 1
                            # a = [w for w in range(len(res.algorithm.callback.data['fitness'][i])) if res.algorithm.callback.data['fitnessTime'][i][w] + res.algorithm.callback.data['fitnessSlide'][i][w] + res.algorithm.callback.data['fitnessDiscrete'][i][w] + res.algorithm.callback.data['fitnessBlockages'][i][w] in res.algorithm.callback.data['fitness'][i]]
                            # print(a)
                            writer.writerow([numSeed, res.algorithm.callback.data['gen'][i], nfe,
                                             res.algorithm.callback.data['individuals'][i][x].tolist(),
                                             res.algorithm.callback.data['fitness'][i][x][0],
                                             res.algorithm.callback.data['fitnessTime'][i][x][0],
                                             res.algorithm.callback.data['fitnessSlide'][i][x][0],
                                             res.algorithm.callback.data['fitnessDiscrete'][i][x][0],
                                             res.algorithm.callback.data['fitnessBlockages'][i][x][0],
                                             res.algorithm.callback.data['fitnessCycleHS'][i][x][0],
                                             res.algorithm.callback.data['wallTimeSimulInd'][i][x][0],
                                             res.algorithm.callback.data['procTimeSimulInd'][i][x][0],
                                             res.algorithm.callback.data['wallTimeEvalInd'][i][x][0],
                                             res.algorithm.callback.data['procTimeEvalInd'][i][x][0]])
                if config['debug']:
                    print("> pop_info_level.CSV created")
            else:
                with open(subRootSavePath + 'pop_info_level.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    nfe = 0
                    for i in range(len(res.algorithm.callback.data['individuals'])):
                        # for ind in individuals
                        for x in range(len(res.algorithm.callback.data['individuals'][i])):
                            nfe += 1
                            writer.writerow([numSeed, res.algorithm.callback.data['gen'][i], nfe,
                                             res.algorithm.callback.data['individuals'][i][x].tolist(),
                                             res.algorithm.callback.data['fitness'][i][x][0],
                                             res.algorithm.callback.data['fitnessTime'][i][x][0],
                                             res.algorithm.callback.data['fitnessSlide'][i][x][0],
                                             res.algorithm.callback.data['fitnessDiscrete'][i][x][0],
                                             res.algorithm.callback.data['fitnessBlockages'][i][x][0],
                                             res.algorithm.callback.data['fitnessCycleHS'][i][x][0],
                                             res.algorithm.callback.data['wallTimeSimulInd'][i][x],
                                             res.algorithm.callback.data['procTimeSimulInd'][i][x],
                                             res.algorithm.callback.data['wallTimeEvalInd'][i][x],
                                             res.algorithm.callback.data['procTimeEvalInd'][i][x]])
                #     for i in range(len(res.algorithm.callback.data['individuals'])):
                #         for x in range(len(res.algorithm.callback.data['individuals'][i])):
                #             nfe+=1
                #             writer.writerow([NUM_SEED, res.algorithm.callback.data['gen'][i], nfe, res.algorithm.callback.data['individuals'][i][x], res.algorithm.callback.data['fitness'][i][x],res.algorithm.callback.data['fitnessTime'][i][x], res.algorithm.callback.data['fitnessSlide'][i][x], res.algorithm.callback.data['fitnessDiscrete'][i][x], res.algorithm.callback.data['fitnessBlockages'][i][x]])
                if config['debug']:
                    print("> pop_info_level.CSV appended")

            # GEN LEVEL
            fieldnames = ['seed', 'gen', 'worst', 'avg', 'best', 'std', 'gen_std']
            if (not (os.path.isfile(subRootSavePath + 'gen_info_level.csv'))):
                with open(subRootSavePath + 'gen_info_level.csv', 'w') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(fieldnames)
                    for i in range(len(res.algorithm.callback.data['best'])):
                        writer.writerow([numSeed, res.algorithm.callback.data['gen'][i],
                                         res.algorithm.callback.data['worst'][i], res.algorithm.callback.data['avg'][i],
                                         res.algorithm.callback.data['best'][i], res.algorithm.callback.data['std'][i],
                                         res.algorithm.callback.data['gen_std'][i]])
                if config['debug']:
                    print("> gen_info_level.CSV created")
            else:
                with open(subRootSavePath + 'gen_info_level.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    for i in range(len(res.algorithm.callback.data['best'])):
                        writer.writerow([numSeed, res.algorithm.callback.data['gen'][i],
                                         res.algorithm.callback.data['worst'][i], res.algorithm.callback.data['avg'][i],
                                         res.algorithm.callback.data['best'][i], res.algorithm.callback.data['std'][i],
                                         res.algorithm.callback.data['gen_std'][i]])
                if config['debug']:
                    print("> gen_info_level.CSV appended")

            # 15. Save data about the performances time by generation for diferent granularities: simul ind, eval ind {min, max, avg, std} eval pop {walltime, cputime}
            fieldnames = ['seed', 'gen', 'wallTimeSimulIndMin', 'wallTimeSimulIndMax', 'wallTimeSimulIndAvg',
                          'wallTimeSimulIndStd', 'procTimeSimulIndMin', 'procTimeSimulIndMax', 'procTimeSimulIndAvg',
                          'procTimeSimulIndStd', 'wallTimeEvalIndMin', 'wallTimeEvalIndMax', 'wallTimeEvalIndAvg',
                          'wallTimeEvalIndStd', 'procTimeEvalIndMin', 'procTimeEvalIndMax', 'procTimeEvalIndAvg',
                          'procTimeEvalIndStd']
            if (not (os.path.isfile(subRootSavePath + 'time_info_gen.csv'))):
                with open(subRootSavePath + 'time_info_gen.csv', 'w') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(fieldnames)
                    for i in range(len(res.algorithm.callback.data['gen'])):
                        writer.writerow([numSeed, res.algorithm.callback.data['gen'][i],
                                         res.algorithm.callback.data['wallTimeSimulIndMin'][i],
                                         res.algorithm.callback.data['wallTimeSimulIndMax'][i],
                                         res.algorithm.callback.data['wallTimeSimulIndAvg'][i],
                                         res.algorithm.callback.data['wallTimeSimulIndStd'][i],
                                         res.algorithm.callback.data['procTimeSimulIndMin'][i],
                                         res.algorithm.callback.data['procTimeSimulIndMax'][i],
                                         res.algorithm.callback.data['procTimeSimulIndAvg'][i],
                                         res.algorithm.callback.data['procTimeSimulIndStd'][i],
                                         res.algorithm.callback.data['wallTimeEvalIndMin'][i],
                                         res.algorithm.callback.data['wallTimeEvalIndMax'][i],
                                         res.algorithm.callback.data['wallTimeEvalIndAvg'][i],
                                         res.algorithm.callback.data['wallTimeEvalIndStd'][i],
                                         res.algorithm.callback.data['procTimeEvalIndMin'][i],
                                         res.algorithm.callback.data['procTimeEvalIndMax'][i],
                                         res.algorithm.callback.data['procTimeEvalIndAvg'][i],
                                         res.algorithm.callback.data['procTimeEvalIndStd'][i]])
                if config['debug']:
                    print("> representatives.CSV created")
            else:
                with open(subRootSavePath + 'time_info_gen.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    for i in range(len(res.algorithm.callback.data['gen'])):
                        writer.writerow([numSeed, res.algorithm.callback.data['gen'][i],
                                         res.algorithm.callback.data['wallTimeSimulIndMin'][i],
                                         res.algorithm.callback.data['wallTimeSimulIndMax'][i],
                                         res.algorithm.callback.data['wallTimeSimulIndAvg'][i],
                                         res.algorithm.callback.data['wallTimeSimulIndStd'][i],
                                         res.algorithm.callback.data['procTimeSimulIndMin'][i],
                                         res.algorithm.callback.data['procTimeSimulIndMax'][i],
                                         res.algorithm.callback.data['procTimeSimulIndAvg'][i],
                                         res.algorithm.callback.data['procTimeSimulIndStd'][i],
                                         res.algorithm.callback.data['wallTimeEvalIndMin'][i],
                                         res.algorithm.callback.data['wallTimeEvalIndMax'][i],
                                         res.algorithm.callback.data['wallTimeEvalIndAvg'][i],
                                         res.algorithm.callback.data['wallTimeEvalIndStd'][i],
                                         res.algorithm.callback.data['procTimeEvalIndMin'][i],
                                         res.algorithm.callback.data['procTimeEvalIndMax'][i],
                                         res.algorithm.callback.data['procTimeEvalIndAvg'][i],
                                         res.algorithm.callback.data['procTimeEvalIndStd'][i]])
                if config['debug']:
                    print("> time_info_gen.CSV appended")

            # 16. Plot the monotonic convergence curve
            plt.title("Convergence")
            plt.plot(res.algorithm.callback.data['n_evals'], res.algorithm.callback.data['opt'], "-")
            plt.yscale("log")
            plt.xlabel("NFE")
            plt.ylabel("log(optimum)")
            plt.savefig(savePath + 'convergence')
            plt.clf()
            if config['visualise']:
                plt.show()

            # 17. Plot the gen_std curve
            plt.title("Gen std")
            plt.plot(res.algorithm.callback.data['n_evals'], res.algorithm.callback.data['gen_std'], '-')
            plt.xlabel("NFE")
            plt.ylabel("STD(pop)")
            plt.savefig(savePath + 'deviation_standard')
            plt.clf()
            if config['visualise']:
                plt.show()

            # 1-bis-bis Plot the boxplot evolution (population/generation) TODO
            # df = pd.DataFrame(data=np.array(res.algorithm.callback.data["individuals"]), index= res.algorithm.callback.data['n_evals'])
            # data = [i.tolist() for i in res.algorithm.callback.data["individuals"]]
            # print(len(res.algorithm.callback.data['gen_std']))
            # print(res.algorithm.callback.data['gen_std'][0])
            # plt.boxplot(res.algorithm.callback.data['gen_std'], positions=res.algorithm.callback.data['n_evals'])

            idxsTabOfCelsToOptForThisRun = idxsTabOfCelsToOpt
            # 18.a Save the best individual obtained during the run in terms of solutions and objectives
            X = res.X
            F = res.F
            if config['debug']:
                print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
            utils.save_single_best_sol(savePath, "solution", X.tolist(), F.tolist(), config['debug'])
            utils.save_single_best_sol_csv(savePath, "solution", X.tolist(), F.tolist(), config['debug'])
            # 18.b Simulate the best solution
            utils.create_directory('solution_simulated', os.getcwd() + '/' + savePath)
            simulator.reset()
            if idxsTabOfCelsToOptForThisRun is not None:
                a = 0
                for idxCel in range(len(allCels)):
                    if idxCel in idxsTabOfCelsToOptForThisRun:
                        simulator.getAllCelerities()[idxCel].setValue(X[a])
                        a += 1
            else:
                simulator.setCeleritiesValue(X)
            simulator.simulation()
            utils.save_trace(savePath + 'solution_simulated/', 'sol', simulator.getTrace(), config['debug'])
            # ADD A PARAMETER HERE like save_in_graph
            if len(variables) < 4:
                utils.save_trace_for_visu_2_3D(savePath + 'solution_simulated/', 'sol_for_visu', simulator.getTrace(),
                                               config['debug'])
            else:
                utils.save_trace_for_visu_3D_plus(savePath + 'solution_simulated/', 'sol_for_visu', variables,
                                                  simulator.getTrace(), config['debug'])

            # 19.a Save the final population
            pop = res.pop
            # print(pop.get("X"))
            # print(pop.get("F"))
            utils.save_evaluated_population(savePath, "last_pop", pop.get("X").tolist(), pop.get("F").tolist(),
                                            config['debug'])
            utils.save_evaluated_population_csv(savePath, "last_pop", pop.get("X").tolist(), pop.get("F").tolist(),
                                                config['debug'])
            # 19.b if needed: Simulate the solutions of last pop
            utils.create_directory('last_pop_simulated', os.getcwd() + '/' + savePath)
            i = 0
            for x in pop.get("X"):
                simulator.reset()
                if idxsTabOfCelsToOptForThisRun is not None:
                    a = 0
                    for idxCel in range(len(allCels)):
                        if idxCel in idxsTabOfCelsToOptForThisRun:
                            simulator.getAllCelerities()[idxCel].setValue(x[a])
                            a += 1
                else:
                    simulator.setCeleritiesValue(x)
                # simulator.simulateDispiteBlockagesAndBadTransitions(len(BK[-2]), 48., 0., -1, simulator.getVariables(), simulator.getInitialHybridState(), simulator.getAllCelerities())
                simulator.simulation()
                utils.save_trace(savePath + 'last_pop_simulated/', 'sol' + str(i), simulator.getTrace(),
                                 config['debug'])
                if len(variables) < 4:
                    utils.save_trace_for_visu_2_3D(savePath + 'last_pop_simulated/', 'sol' + str(i) + '_for_visu',
                                                   simulator.getTrace(), config['debug'])
                else:
                    utils.save_trace_for_visu_3D_plus(savePath + 'last_pop_simulated/', 'sol' + str(i) + '_for_visu',
                                                      variables, simulator.getTrace(), config['debug'])
                i += 1

            # 20. Time execution of the algorithm and the run time
            print("The time required to run the algorithm is %s s ===\n" % (res.exec_time))
            utils.save_time(savePath, 'alg', '', res.exec_time, config['debug'])

            print("=== The time required to execute this run is %s s ===\n" % (elapsedWallTimeRun))
            utils.save_time(savePath, 'run', '', elapsedWallTimeRun, config['debug'])

    # if seeds had to be changed
    # utils.save_seeds_modify(config['results_dir_name']+'/'+config['experiment_dir_name']+'/', SEEDS, config['debug'])

    # Stop the execution wall time clock for the experiment and save it
    elapsedWallTimeExperiment = datetime.now() - startWallTimeExperiment
    print("FULL RUNS TIME --- %s seconds ---" % (elapsedWallTimeExperiment))
    utils.save_time(config['results_dir_name'] + "/" + config['experiment_dir_name'] + "/", 'runs', '',
                    elapsedWallTimeExperiment, config['debug'])
    # utils.save_time_full_run(config['results_dir_name']+"/"+config['experiment_dir_name']+"/", elapsedWallTimeExperiment, config['debug'])

    ### FINAL INFORMATION SAVED ###
    # Create or append CSV file
    fieldnames = ['name', 'algorithm', 'problem', 'n_tests', 'date']
    if (not (os.path.isfile(config['results_dir_name'] + '/experiments.csv'))):
        with open(config['results_dir_name'] + '/experiments.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            writer.writerow(
                [config['experiment_dir_name'], config['algorithm'], str(problem.pBname), str(config['n_test']),
                 str(datetime.now())])
        if config['debug']:
            print("> experiments.CSV created")
    else:
        with open(config['results_dir_name'] + '/experiments.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [config['experiment_dir_name'], config['algorithm'], str(problem.pBname), str(config['n_test']),
                 str(datetime.now())])
        if config['debug']:
            print("> experiments.CSV appended")

    # close the pool of processes
    pool.close()