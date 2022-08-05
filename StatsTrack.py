# import pandas module 
import pandas as pd 
import matplotlib.pyplot as plt
    
# making dataframe 
df = pd.read_csv("microbench.csv") 
   
# output the dataframe
print(df)

# plotting a bar graph
plt.bar(df["Benchmark"], df["IPC"])
plt.show()