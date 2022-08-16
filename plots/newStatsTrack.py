import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

prefixes = ['CC', 'CF', 'CR', 'CS', 'DP', 'ED', 'EF', 'EI', 'EM', 'MC', 'MD', 'MI', 'ML', 'MM', 'M_', 'ST']

data = {}
data_sorted = {}

# making dataframe
df1 = pd.read_csv("perf_microbench.csv")
X = df1["Benchmark"]
Y1 = df1["IPC"]
Y2 = df1["Cycles"]
Y3 = df1["Instructions"]

df2 = pd.read_csv("gem5runs_microbench.csv")
X_2 = df2["Benchmark"]
Y1_2 = df2["IPC"]
Y2_2 = df2["Cycles"]
Y3_2 = df2["Instructions"]

with open("microbench_cycles_diff.csv", "w") as csvfile:
    filewriter = csv.writer(
        csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )
    filewriter.writerow(["name", "perf", "gem5", "% difference"])
    csvfile.close()

def plot(stat):
    i = 0
    j = 0

    for b, bench in enumerate(X):
        diff = (df2[stat].iloc[b] - df1[stat].iloc[b])
        data[bench] = diff
        with open("microbench_cycles_diff.csv", "a") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            filewriter.writerow([bench, df1[stat].iloc[b], df2[stat].iloc[b], diff])
            csvfile.close()
    
    keys = sorted(data, key=data.get)
    for r in keys:
        data_sorted[r] = [data[r]]


    # match a key from dictionary to an array of prefixes
    for k, v in data_sorted.items():
        for p in prefixes:
            if k.startswith(p):
                data_sorted[k].append(prefixes.index(p))
    
    print(data_sorted)

    for b, bench in data_sorted.items():
        plt.bar(i, data_sorted[b][0], 0.2, color="C" + str(data_sorted[b][1]))
        i = i + 1
    
    for i, pfrm in enumerate(prefixes):
        plt.bar(0, 0, color="C" + str(i), label=pfrm)
    
    plt.xticks((np.arange(len(data_sorted))), data_sorted, rotation=80, ha="center", fontsize=11)

    plt.xlabel("Benchmarks")
    plt.ylabel(stat)
    plt.title("Benchmark vs. " + stat)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.show()


plot("IPC")
