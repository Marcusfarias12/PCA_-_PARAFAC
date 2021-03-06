import numpy as np
import pandas as pd
import tensorly as tl
from tensorly.decomposition import parafac
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.decomposition import PCA
import os
from new import csv_to_excel
from matplotlib.pyplot import figure
figure(figsize=(8, 6), dpi=100)

path_original_data = r"{}".format(str(input("Input the directory of the original data (in .csv to converto to .xlsx): ")))

path = r"{}".format(str(input("Input the directory that has all the data that will be used in PCA (in .xlsx): ")))

save = input("Save in .xlsx? [y,n] ")
if save == 'y':
    csv_to_excel(path_original_data, path)

files = os.listdir(path)
for files in os.walk(path, topdown = False):
    list = files[2]

print("\n The files are: \n")
for i in range(0, len(files[2])):
    print("File {}".format(i),files[2][i])


number = int(input("\nHow many files? "))

names = []
for i in range(0,number):
  w = int(input("Input the number of the file you want: "))
  names.append(files[2][w])

d = {}
l = []
for x in range(0, len(names)):
    d["data{}".format(names[x])] = pd.read_excel(path +'/{}'.format(names[x]), header=None, engine='openpyxl', skiprows=1)
    d["data{}".format(names[x])] = pd.DataFrame(data = d["data{}".format(names[x])].dropna().values)
    d["data{}".format(names[x])] = d["data{}".format(names[x])].apply(pd.to_numeric, errors='coerce')
    l.append(len(d["data{}".format(names[x])][0]))
data = pd.DataFrame(data = [d["data{}".format(f)][2][:min(l)] for f in names])
print(data)
if data.empty:
    print("Error! Empty Dataframe")
rank = int(input("Input the rank value: "))
X_scaled = preprocessing.scale(data)
pca = PCA(n_components=rank)
principalComponents = pca.fit_transform(X_scaled)

PCA = pd.DataFrame(data=principalComponents, columns = ["component{}".format(f+1) for f in range(0, rank)])
list = [pca.explained_variance_ratio_[f]*100 for f in range(0, rank)]
print("The cumulative error is: ", sum(list), "%")

for i in range(0,len(names)):
    if names[i].endswith('.xlsx'):
        names[i] = names[i][:-5]

df = pd.concat([PCA,  pd.Series(names).rename('Samples')] ,axis=1)
print("\n The sheet is: \n ",df)

if rank == 3:
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    plot = str(input("Plot? (y/n) "))
    if plot == "y":
        for i in range(0, len(df)):
            if "Amido" in df["Samples"][i]: ###ATENTION!!!
                ax.scatter(df["component1"][i],df["component2"][i],df["component3"][i], label = df["Samples"][i])# , c = "m")
            else:
                ax.scatter(df["component1"][i],df["component2"][i],df["component3"][i], label=df["Samples"][i])#, c="g")
        ax.set_title("PCA - 3 Components")
        ax.set_xlabel("Component 1({}%)".format(round(list[0], 2)))
        ax.set_ylabel("Component 2({}%)".format(round(list[1], 2)))
        ax.set_zlabel("Component 3({}%)".format(round(list[2], 2)))
        ax.legend(loc = 'best', prop={'size': 6})
        ax.grid()
        plt.show()
        print("Done!")
    else:
        df.to_excel("PCA_{}Components.xlsx".format(rank))
        print("The file was saved successfully with {}".format(rank), "Components")
elif rank ==2:
    plot = str(input("Plot? (y/n) "))
    if plot == "y":
        for i in range(0, len(df)):
            if "Amido" in df["Samples"][i]: ##AMIDO
                plt.scatter(PCA["component1"][i], PCA["component2"][i], label = df["Samples"][i], c = "gold") #, c = "gold")
            else:
                plt.scatter(PCA["component1"][i], PCA["component2"][i], label=df["Samples"][i],c ="c")#, c="c")
        plt.title("PCA - 2 Components")
        plt.xlabel("Component 1({}%)".format(round(list[0], 2)))
        plt.ylabel("Component 2({}%)".format(round(list[1], 2)))
        plt.legend(loc = 'best')
        plt.grid()
        plt.show()
        print("Done!")
    else:
        df.to_excel("PCA_{}Components.xlsx".format(rank))
        print("The file was saved successfully with {}".format(rank), "Components")
else:
    df.to_excel("PCA_{}Components.xlsx".format(rank))
    print("The file was saved successfully with {}".format(rank), "Components")

