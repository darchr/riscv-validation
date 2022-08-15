# import pandas module 
from turtle import color
import pandas as pd 
import matplotlib.pyplot as plt
    
# making dataframe 
df1 = pd.read_csv("perf_microbench.csv") 
df2 = pd.read_csv("gem5_microbench.csv") 
   
# output the dataframe
print(df1)
print(df2)

# plotting a bar graph
plt.bar(df1["Benchmark"], df1["IPC"], color= 'blue')
plt.show()
plt.bar(df1["Benchmark"], df1["Cycles"])
plt.show()