import os
import configparser
from parser.parse import Parser
from simulator.utils import *
from simulator.hybridstate import *
import utils.utils as utils
import csv


def create_directory(name: str, defaultpath=os.getcwd() + '/') -> None:
    """
    Create the directory in which the results of the framework will be saved.
    """
    path = defaultpath + name
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed\n" % path)
    else:
        print("Successfully created the directory %s \n" % path)


### Read seeds file ###
def parse_seeds(name: str, path: str) -> None:
    lines = []
    with open(path + name) as f:
        lines = [int(line.rstrip()) for line in f]
    return lines


def parse_seeds_csv(name: str, path: str) -> None:
    rows = []
    with open(path + name + '.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row[0])
    return rows


### ______________ ###

def save_trace(path: str, nameOfFile: str, trace, debug: bool) -> None:
    """
    Save trace into file.
    """
    with open(path + nameOfFile + '.txt', 'w') as f:
        for path in trace:
            f.write(str(path[0]) + " " + str(path[1]) + "\n")
    if debug:
        print('>' + nameOfFile + '.txt saved\n')


def save_trace_for_visu_2_3D(path: str, nameOfFile: str, trace, debug: bool) -> None:
    """
    Save trace into csv for visualization 2 or 3D.
    """
    with open(path + nameOfFile + '.csv', 'w') as f:
        writer = csv.writer(f)
        for path in trace:
            writer.writerow([path[0]] + path[1].getDiscreteState() + path[1].getFractionalPart())
            # f.write(str(path[0]) + " " + str(path[1]) + "\n")
    if debug:
        print('>' + nameOfFile + '.txt saved\n')


def save_trace_for_visu_3D_plus(path: str, nameOfFile: str, variables, trace, debug: bool) -> None:
    """
    Save trace into csv for visualization for 3D+.
    """
    strVars = "Time"
    for var in variables:
        strVars += " " + var.getName()
    strVars += "\n"
    with open(path + 'graph_data_' + nameOfFile + '.txt', 'w') as f:
        f.write(strVars)
        for path in trace:
            variablesCon = ''
            for i in range(len(variables)):
                variablesCon += str(float(path[1].getDiscreteState()[i] + path[1].getFractionalPart()[i])) + ' '
            f.write(str(path[0]) + ' ' + variablesCon + '\n')


# ____________
def save_population(path: str, nameOfFile: str, X: list, debug: bool = False) -> None:
    """
    Save population data.
    """
    with open(path + nameOfFile + '.txt', 'w') as f:
        for i in range(len(X)):
            f.write(str(X[i]) + '\n')
    if debug:
        print('>' + nameOfFile + '.txt saved\n')


def save_population_csv(path: str, nameOfFile: str, population: list, debug: bool) -> None:
    """ 
    Save individuals from population in csv.
    """
    with open(path + nameOfFile + '.csv', 'w') as f:
        writer = csv.writer(f)
        for i in range(len(population)):
            writer.writerow(population[i])
    if debug:
        print('>' + nameOfFile + '.csv saved\n')


# ________________

# ____________
def save_evaluated_population(path: str, nameOfFile: str, X: list, F: list, debug: bool) -> None:
    """
    Save individuals from population.
    """
    with open(path + nameOfFile + '.txt', 'w') as f:
        for i in range(len(X)):
            f.write('Solution: ' + str(X[i]) + ' Objective: ' + str(F[i][0]) + '\n')
    if debug:
        print('>' + nameOfFile + '.txt saved\n')


def save_evaluated_population_csv(path: str, nameOfFile: str, population: list, fitnesses: list, debug: bool) -> None:
    """ 
    Save individuals from population in csv.
    """
    with open(path + nameOfFile + '.csv', 'w') as f:
        writer = csv.writer(f)
        for i in range(len(population)):
            writer.writerow(population[i] + fitnesses[i])
    if debug:
        print('>' + nameOfFile + '.csv saved\n')


# ________________

# ____________
def save_single_best_sol(path: str, nameOfFile: str, X: list, F: list, debug: bool) -> None:
    """
    Save problem solution.
    """
    with open(path + nameOfFile + '.txt', 'w') as f:
        f.write('Solution: ' + str(X) + ' Objective: ' + str(F[0]) + '\n')
    if debug:
        print('>' + nameOfFile + '.txt saved\n')


def save_single_best_sol_csv(path: str, nameOfFile: str, solution: list, fitness: list, debug: bool) -> None:
    """
    Save problem solution in csv.
    """
    with open(path + nameOfFile + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(solution + fitness)
    if debug:
        print('>' + nameOfFile + '.csv saved\n')


# ________________

# def save_time(path:str, type:str, timeExecution, debug:bool) -> None:
#     """
#     Save execution time.
#     type is {alg, run, runs, exp}
#     """
#     with open(path+type+'_time.txt', 'w') as f:
#         f.write("The time required to execute the " + type + " is %s s." % (timeExecution))
#     if debug:
#         print('> time.txt saved\n')

def save_time(path: str, type: str, pos: str, timeExecution, debug: bool) -> None:
    """
    Save execution time.
    type is {alg, run, runs, exp}
    """
    with open(path + type + '_time_' + pos + '.txt', 'w') as f:
        f.write("The time required to execute the " + type + " is %s s." % (timeExecution))
    if debug:
        print('> time.txt saved\n')


def save_seeds(pathToSave: str, seedsList: list[int], debug: bool) -> None:
    """
    Save the seeds generated for the different test executions
    """
    with open(pathToSave + 'seeds.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['seeds'])
        for seed in seedsList:
            writer.writerow([seed])
    if debug:
        print("> seeds.csv saved")


# def save_seeds_modify(path:str, seedsList:list[int], debug:bool) -> None:
#     """
#     Modify the seeds for the different test executions
#     """
#     with open(path+'mod_seeds.txt', 'w') as f:
#         for seed in seedsList:
#             f.write(str(seed)+'\n')
#     if debug:
#         print("> Modified seeds saved")


def import_settings_configuration(config_file):
    """
    Read the config file regarding the experiment settings and import its content
    """
    content = configparser.ConfigParser()
    content.read(config_file)
    config = {}
    config['smb'] = content['hgrn']['smb']
    config['n_test'] = content['test'].getint('n')
    config['from'] = content['test'].getint('from')

    config['cp'] = content['type'].getboolean('cp')
    config['coevo'] = content['type'].getboolean('coevo')
    config['decompositionType'] = content['type']['decompositionType']

    config['algorithm'] = content['soea']['algorithm'].split()
    config['population_size'] = content['soea'].getint('population_size')
    config['objectives'] = content['soea'].getint('objectives')
    # config['variables'] = content['moea'].getint('variables')
    config['celerities_range'] = content['soea'].getint('celerities_range')
    config['constraints'] = content['soea'].getint('constraints')
    config['evaluations'] = content['soea'].getint('evaluations')
    config['from_checkpoint'] = content['soea']['from_checkpoint']

    config['criteria'] = content['fitness'].getint('criteria')
    config['type'] = content['fitness']['type']

    config['results_dir_name'] = content['dir']['results_dir_name']
    config['experiment_dir_name'] = content['dir']['experiment_dir_name']

    config['visualise'] = content['options'].getboolean('visualise')
    config['debug'] = content['options'].getboolean('debug')
    config['readable'] = content['options']['readable']

    return config


def import_analysis_configuration(config_file):
    """
    Read the config file regarding the experiment analysis and import its content
    """
    content = configparser.ConfigParser()
    content.read(config_file)
    config = {}
    # config['coevo'] = content['settings'].getboolean('coevo')
    config['coevo'] = content['settings']['coevo'].split()
    config['algorithms'] = content['settings']['algorithm'].split()
    config['nb_runs'] = content['settings'].getint('n')
    config['paths'] = content['settings']['path'].split()

    config['typeOfPlots'] = content['plots']['typeOfPlot'].split()

    config['typeOfPrints'] = content['prints']['typeOfPrint'].split()
    config['epsilon'] = content['prints'].getfloat('valid')

    config['stat_tests'] = content['stat_tests'].getboolean('run')
    config['alpha'] = content['stat_tests'].getfloat('alpha')

    return config


def parse(settingFile: str, debug: bool = False):
    """
    Method to parse the smb config file and returns the variables and the biological knowledge.
    """

    # Influence Graph informations
    par = Parser("smbFiles/", settingFile, 0)  # 1 for info
    visitor = par.parse()

    if debug:
        print("\n**** Parsed information ****\n")
    variables = visitor.getVarBlock().getData()
    if debug:
        print(len(variables))
        for var in variables:
            print(var)

    # Regulations
    multiplexes = visitor.getRegBlock().getRegs()
    if debug:
        for mult in multiplexes:
            print(mult)

    # for var in variables:
    #     print(var.getPredecessors())

    # Biological knowledge with hybrid hoare logic
    if visitor.getHybridHoareBlock().isCyclic():
        if debug:
            print("Cyclic behavior")
        visitor.getHybridHoareBlock().setPreCondition(visitor.getHybridHoareBlock().getPostCondition())
    initialHybridState = visitor.getHybridHoareBlock().getPreCondition()
    if debug:
        print("Initial Hybrid State :", initialHybridState)

    trace = visitor.getHybridHoareBlock().getTrace()
    if debug:
        for ep in trace:
            print(ep)

    finalHybridState = visitor.getHybridHoareBlock().getPostCondition()
    if debug:
        print("Final Hybrid State :", finalHybridState)

    # Biological knowledge transformation for fitness eval
    if debug:
        print("\n**** Biological knowledge for fitness evaluation ****\n")
    BK = visitor.getHybridHoareBlock().generateComparatorsListForFitnessEval()
    if debug:
        for i in range(len(BK)):
            info = BK[i]
            if i == len(BK) - 1:
                for j in info:
                    print(j)
            else:
                print(info)

    return variables, multiplexes, initialHybridState, finalHybridState, BK


def getInfosForCoevo(settingFile: str, reduct: bool = True):
    """
    Get some infos for the cooperative coevolution part.
    """

    variables, _, _, _, BK = parse(settingFile)

    allCelerities = generateAllCelerities(variables)
    # this bool just asks for celerities only invilved in the trajectory (from BK) => reduce the search space
    if reduct:
        celsToOpt = generateCeleritiesToOptimize(BK[4], variables)
        idxsTabOfCelsToOpt = getIdxsOfCelToOptimize(allCelerities, celsToOpt)
    discreteStates = generateAllDiscreteStates(variables)
    # list of all celerities that have no doubles and, if reduct, are involved in the trajectory
    globalListCelerities = []
    # list state by state
    listCeleritiesPerState = []
    i = 0
    for d in discreteStates:
        groupC = []
        celerities = HybridState(d, [0.] * len(variables)).getCeleritiesInDiscreteState(variables, allCelerities)
        for c in celerities:
            if all(not (c.same(x)) for x in globalListCelerities) and (
            not (all(not (c.same(x)) for x in celsToOpt)) if reduct else True):
                globalListCelerities.append(c)
                groupC.append(c)
            i += 1
        listCeleritiesPerState.append(groupC)

    # print("*** FOR STATE ***")
    tab = [len(i) for i in listCeleritiesPerState]
    tabState = [i for i in tab if i != 0]

    # print("*** FOR GENE ***")
    nbGenes = len(variables)
    tabGene = [0] * nbGenes
    tabRecompoGene = []
    for c in globalListCelerities:
        for v in variables:
            if c.getVariableName() == v.getName():
                # print(c)
                tabGene[v.getId()] += 1
                tabRecompoGene.append(v.getId())

    return tabState, tabGene, tabRecompoGene, idxsTabOfCelsToOpt


def getParamsForRecombination(file: str):
    """Get the information relative to the experiment for creating a complete sol"""
    config = utils.import_settings_configuration(config_file=file)

    tabState, tabGene, tabRecompoGene, _ = getInfosForCoevo(config['smb'])

    if config['decompositionType'] == 'state':
        return tabState, [i for i in range(len(tabState)) for _ in range(tabState[i])]
    elif config['decompositionType'] == 'gene':
        return tabGene, tabRecompoGene
    else:
        raise ("This kind of decomposition is not known ! => {state | gene}")


def getParamsOfCoevoExperiment(file: str):
    """Get the information relative to the experiment"""
    config = utils.import_settings_configuration(config_file=file)

    tabState, tabGene, _, _ = getInfosForCoevo(config['smb'])

    if config['decompositionType'] == 'state':
        return tabState
    elif config['decompositionType'] == 'gene':
        return tabGene
    else:
        raise ("This kind of decomposition is not known ! => {state | gene}")


def getIdxsOfCelToOptimize(allCelerities: list[Celerity], celsToOpt: list[Celerity]):
    """
    Get idxs of celerities to optimize (when considering the cartesian product of all discrete states and then the celerities (allCelerities) 
    it might have celerities that are not necessary for the celerities extracted from BK (celsToOpt))
    """
    idxTabToRecover = []
    for idxCels in range(len(allCelerities)):
        for celToOpt in celsToOpt:
            if celToOpt.same(allCelerities[idxCels]):
                idxTabToRecover.append(idxCels)
                break
    return idxTabToRecover


def split_bounds(listOfElements, splitter=":", debug=False):
    from fractions import Fraction
    SAFE_EPSILON = 1e-3
    varsName = []
    minBounds = []
    maxBounds = []
    for el in listOfElements:
        vars = el.split(splitter)
        name = vars[0]
        varsName.append(name)
        values = vars[1]
        minBound, maxBound = values.split(';')
        minBoundAcc = minBound[0]
        minBound = minBound[1:]
        if "/" in minBound:
            minBound = Fraction(minBound)
        # if minBoundAcc == "]":
        minBounds.append(float(minBound) - SAFE_EPSILON)
        # else:
        #    minBounds.append(float(minBound))
        maxBoundAcc = maxBound[-1]
        maxBound = maxBound[:-1]
        if "/" in maxBound:
            maxBound = Fraction(maxBound)
        # if maxBoundAcc == "[":
        maxBounds.append(float(maxBound) + SAFE_EPSILON)
        # else:
        #   maxBounds.append(float(maxBound))
        if debug:
            print(name, " = ", minBoundAcc, " ", minBounds[-1], ' ; ', maxBounds[-1], ' ', maxBoundAcc)
    if debug:
        print("Number of celerities from the CSP: ", len(listOfElements))
    return varsName, minBounds, maxBounds


def launch_solver(file: str, path_name: str, nbOfSols: int = 10, precision: float = 1e-3, timeMax: int = 24):
    # ./modelling.sh -i ./examples/path_test -n 100 -t 24 -o ./examples/results_romain/res_path_test_100_24/result
    os.system(
        "cd /home/romain/Applications/HolmesBioNet/; sudo ./modelling.sh -i ./examples/path_" + file + " -p " + str(
            precision) + " -n " + str(nbOfSols) + " -t " + str(timeMax) + " -o ./examples/" + path_name + "/result")


def extract_celerities(dir: str, nbSols: int):
    os.system("./extract_celerities.sh " + str(dir))
    surecels = []
    unsurecels = []
    for i in range(1, nbSols + 1):
        # sure celerities
        with open(dir + '/boxes/sure' + str(i)) as f:
            lines = [line.rstrip() for line in f]
        surecels.append(split_bounds(lines, ":", False))
        # not sure celerities
        with open(dir + '/boxes/unsure' + str(i)) as f:
            lines = [line.rstrip() for line in f]
        unsurecels.append(split_bounds(lines, ":", False))
    return surecels, unsurecels


def extract_celerities_from_box_number(dir: str, nb: int):
    surecels = []
    unsurecels = []
    # sure celerities
    with open(dir + '/boxes/sure' + str(nb)) as f:
        lines = [line.rstrip() for line in f]
    surecels.append(split_bounds(lines, ":", False))
    # not sure celerities
    with open(dir + '/boxes/unsure' + str(nb)) as f:
        lines = [line.rstrip() for line in f]
    unsurecels.append(split_bounds(lines, ":", False))
    return surecels, unsurecels


def launch_solver_s(file: str, path_name: str, seed: int, nbOfSols: int = 10, timeMax: int = 24):
    # ./modelling.sh -i ./examples/path_test -n 100 -t 24 -o ./examples/results_romain/res_path_test_100_24/result
    os.system(
        "cd /home/romain/Applications/HolmesBioNet/; sudo ./modelling.sh -i ./examples/path_" + file + " -n " + str(
            nbOfSols) + " -t " + str(timeMax) + " -s " + str(seed + 123) + " -o ./examples/" + path_name + "/result")