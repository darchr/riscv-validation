import os
import pandas as pd


os.chdir("microbench-out/")
folders = os.listdir(".")

# create a dataframe with folders
df = pd.DataFrame(columns=['Benchmark'])

for folder in folders:
    try:
        os.chdir(folder)
        files = os.listdir(".")
        df = pd.concat([df, pd.DataFrame({"Benchmark": [folder]})], ignore_index=True)
        for file in files:
            if file.startswith("stats.txt"):
                with open(file, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        pass
        os.chdir("..")
    except:
        print("error")
        pass

print(df)
