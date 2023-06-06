import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd


def get_dataframe(filename):
    data = []
    with open(filename, 'r') as file:
        print(file)
        for line in file:
            data.append(json.loads(line))
    n_columns = len(data[0])
    data = pd.DataFrame(data, columns=list(range(1, n_columns + 1, 1)))
    melted_df = pd.melt(data)
    return melted_df


# data_lamcts = get_dataframe('../LA-MCTS/Ackleyturbo20/result2000')
data_lamcts_turbo = get_dataframe('arrays_visualize/result1000_ackley_turbo_20')
data_lamcts = get_dataframe('arrays_visualize/result900_ackley_bo_20')
# data_lamcts_de = get_dataframe('arrays_visualize/result200_ackley_de_2')
# data_bo = get_dataframe('../LA-MCTS-baselines/Bayesian-Optimization/Ackley20/result100')
# Plotting using seaborn
sns.lineplot(data=data_lamcts, x='variable', y='value', label='LA-MCTS (BO)')
sns.lineplot(data=data_lamcts_turbo, x='variable', y='value', label='LA-MCTS (TuRBO)')
# sns.lineplot(data=data_lamcts_de, x='variable', y='value', label='LA-MCTS (TuRBO)')
# sns.lineplot(data=data_bo, x='variable', y='value', label='Bayesian Optimization', hue=1, palette=['orange'], linestyle="dashed")

# Set the title and labels for the plot
plt.title('Ackley20')
plt.xlabel('# samples')
plt.ylabel('f(x)')
# Display the plot
# plt.legend()
plt.show()
# sns.lineplot(data.T)
# plt.show()
#
# asdf = []
# with open('../LA-MCTS/Ackley10/result5000', 'r') as file:
#     for line in file:
#         asdf.append(json.loads(line))
# n_columns = len(asdf[0])
# data = pd.DataFrame(asdf, columns=list(range(1, n_columns + 1, 1)))
#
# sns.lineplot(data=asdf)
# plt.title('Ackley10 LA-MCTS TuRBO')
# plt.show()
