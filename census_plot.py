import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set()

if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'census.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)
    sns.jointplot(x=df["n_users"], y=df["n_proposals"], kind='scatter', s=200, color='m', edgecolor="skyblue", linewidth=2)

    plt.show()