import pandas as pd
import matplotlib.pyplot as plt 

 # making dataframe 
df1 = pd.read_csv("perf_microbench.csv")  
X = df1["Benchmark"]
Y1 = df1["IPC"]
Y2 = df1["Cycles"]
  
# # X_axis = np.arange(len(X))
# plt.bar(df1["Benchmark"], df1["IPC"], color= 'blue')
# plt.bar(1, Y1, 0.4, label = X)
  
# plt.xticks(X_axis, X)
# plt.xlabel("Groups")
# plt.ylabel("Number of Students")
# plt.title("Number of Students in each group")
# plt.legend()
# plt.show()

for i in range(len(df1)):
    #print(df1["Benchmark"][i])
    plt.bar(i+0.1, df1["IPC"], 0.2, color= 'blue', label = "Perf " + df1["Benchmark"][i])
    plt.bar(i-0.1, df1["IPC"], 0.2,  color= 'red', label = "gem5 " + df1["Benchmark"][i])
    break


plt.xlabel("Benchmarks")
plt.ylabel("IPC")
plt.title("Benchmark vs. IPC")
plt.legend()
plt.show()