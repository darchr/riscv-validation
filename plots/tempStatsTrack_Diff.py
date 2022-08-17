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

    # if stat == "Cycles" or stat == "Instructions":
    #     fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    #     fig.subplots_adjust(hspace=0.05)  # adjust space between axes

    for b, bench in enumerate(X):
        if stat == 'Cycles' or stat == 'Instructions':
            diff = ((df2[stat].iloc[b] - df1[stat].iloc[b]))/1000000
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
        if stat == 'Cycles' or stat == 'Instructions':
            if data_sorted[b][0] > 10 or data_sorted[b][0] < -10:
                plt.annotate(str(round(data_sorted[b][0], 1)), (i,0), fontsize = 10)
                print(data_sorted[b][0])
                # annotate the value to the graph
            else:
                plt.bar(i, data_sorted[b][0], color="C" + str(data_sorted[b][1]))
        else:
            plt.bar(i, data_sorted[b][0], color="C" + str(data_sorted[b][1]))
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

    # if stat == "Cycles" or stat == "Instructions":
    #     # zoom-in / limit the view to different portions of the data
    #     ax1.set_ylim(15, 80) 
    #     ax2.set_ylim(-10, 10)  # outliers only
    #     ax3.set_ylim(-80, -15)  # most of the data
    #     # outliers only

    #     # hide the spines between ax and ax2
    #     ax1.spines.bottom.set_visible(False)
    #     ax2.spines.top.set_visible(False)
    #     ax2.spines.bottom.set_visible(False)
    #     ax3.spines.top.set_visible(False)
    #     ax1.xaxis.tick_top()
    #     ax1.tick_params(labeltop=False)  # don't put tick labels at the top
    #     ax2.tick_params(bottom=False)
    #     # ax3.xaxis.tick_bottom()

    #     # Now, let's turn towards the cut-out slanted lines.
    #     # We create line objects in axes coordinates, in which (0,0), (0,1),
    #     # (1,0), and (1,1) are the four corners of the axes.
    #     # The slanted lines themselves are markers at those locations, such that the
    #     # lines keep their angle and position, independent of the axes size or scale
    #     # Finally, we need to disable clipping.

    #     d = .5  # proportion of vertical to horizontal extent of the slanted line
    #     kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
    #                 linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    #     ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
    #     ax2.plot([0, 1], [0, 0], transform=ax2.transAxes, **kwargs)
    #     plt.show()

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
    #plt.rcParams["figure.figsize"]=20,10
    plt.show()

absoluteplot('Cycles')