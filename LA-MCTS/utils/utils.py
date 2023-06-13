from parser.parse import Parser


def parse(settingFile: str, debug: bool = False):
    """
    Method to parse the smb config file and returns the variables and the biological knowledge.
    """

    # Influence Graph information
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
