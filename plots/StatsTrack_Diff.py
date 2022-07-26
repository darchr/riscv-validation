import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

#prefixes = ['CC', 'CF', 'CR', 'CS', 'DP', 'ED', 'EF', 'EI', 'EM', 'MC', 'MD', 'MI', 'ML', 'MM', 'M_', 'ST']
prefixes = ['Control', 'Data Parallel', 'Execution', 'Memory', 'Store Intense']
#prefixes = ['control', 'dependency', 'execution']

data = {}
data_sorted = {}

# making dataframe
df1 = pd.read_csv("perf_microbench.csv")
X = df1["Benchmark"]
Y1 = df1["IPC"]
Y2 = df1["Cycles"]
Y3 = df1["Instructions"]
Y4 = df1["Seconds"]
Y5 = df1["IPS"]

df2 = pd.read_csv("gem5runs_microbench.csv")
X_2 = df2["Benchmark"]
Y1_2 = df2["IPC"]
Y2_2 = df2["Cycles"]
Y3_2 = df2["Instructions"]
Y4_2 = df2["Seconds"]
Y5_2 = df2["IPS"]

with open("microbench_seconds_diff.csv", "w") as csvfile:
    filewriter = csv.writer(
        csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )
    filewriter.writerow(["name", "diff"])
    csvfile.close()

def absoluteplot(stat):
    i = 0
    j = 0
    label = stat

    for b, bench in enumerate(X):
        if stat == 'Cycles' or stat == 'Instructions':
            diff = ((df2[stat].iloc[b] - df1[stat].iloc[b]))/1000000
            print(diff)
            label = 'Million ' + stat
        elif stat == 'IPS':
            diff = ((df2[stat].iloc[b] - df1[stat].iloc[b]))/1000000000
            label = 'B' + stat
        else:
            diff = (df2[stat].iloc[b] - df1[stat].iloc[b])
        data[bench] = diff
    
    keys = sorted(data, key=data.get)
    for r in keys:
        data_sorted[r] = [data[r]]

    # match a key from dictionary to an array of prefixes
    for k, v in data_sorted.items():
        for p in prefixes:
            if k.startswith(p[0]):
                data_sorted[k].append(prefixes.index(p))
    
    

    for b, bench in data_sorted.items():
        plt.bar(i, data_sorted[b][0], 0.2, color="C" + str(data_sorted[b][1]))
        with open("microbench_seconds_diff.csv", "a") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            filewriter.writerow([b, data_sorted[b][0]])
            csvfile.close()
        i = i + 1
    
    for i, pfrm in enumerate(prefixes):
        plt.bar(0, 0, color="C" + str(i), label=pfrm)
    
    plt.xticks((np.arange(len(data_sorted))), data_sorted, rotation=80, ha="center", fontsize=14)

    plt.xlabel("Benchmarks")
    plt.ylabel(label)
    plt.axhline(y=0)
    plt.title("Benchmark vs. " + label)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.show()

def percentageplot(stat):
    i = 0
    j = 0

    for b, bench in enumerate(X):
        diff = (df2[stat].iloc[b] - df1[stat].iloc[b])/df1[stat].iloc[b]
        data[bench] = diff
    
    keys = sorted(data, key=data.get)
    for r in keys:
        data_sorted[r] = [data[r]]

    # match a key from dictionary to an array of prefixes
    for k, v in data_sorted.items():
        for p in prefixes:
            if k.startswith(p[0]):
                data_sorted[k].append(prefixes.index(p))
    
    

    for b, bench in data_sorted.items():
        plt.bar(i, data_sorted[b][0], 0.2, color="C" + str(data_sorted[b][1]))
        with open("microbench_seconds_diff.csv", "a") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            filewriter.writerow([b, data_sorted[b][0]])
            csvfile.close()
        i = i + 1
    
    for i, pfrm in enumerate(prefixes):
        plt.bar(0, 0, color="C" + str(i), label=pfrm)
    
    plt.xticks((np.arange(len(data_sorted))), data_sorted, rotation=80, ha="center", fontsize=14)

    plt.xlabel("Benchmarks")
    plt.ylabel(stat)
    plt.axhline(y=0)
    plt.title("Benchmark vs. " + stat)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.show()

absoluteplot('IPS')