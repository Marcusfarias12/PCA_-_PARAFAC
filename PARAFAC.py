import numpy as np
import pandas as pd
import tensorly as tl
from tensorly.decomposition import parafac
import matplotlib.pyplot as plt
import os

from matplotlib.pyplot import figure

figure(figsize=(8, 6), dpi=100)

path =  r"{}".format(str(input("Input the directory: ")))
files = os.listdir(path)
for files in os.walk(path, topdown = False):
    list = files[2]

print("\n The files are: \n")
for i in range(0, len(files[2])):
    print("File {}".format(i),files[2][i])

number = int(input("\n How many files? "))

names = []
for i in range(0,number):
  w = int(input("Input the number of the file you want: "))
  names.append(files[2][w])

d = {}
h = []
l = []
for x in range(0, len(names)):
    d["data{}".format(names[x])] = pd.read_excel (path+'\{}'.format(names[x]), header=None, engine='openpyxl')
    d["data{}".format(names[x])].drop(0, inplace=True, axis=1)
    d["data{}".format(names[x])].to_numpy()
    h.append(len(d["data{}".format(names[x])].index))
    l.append(len(d["data{}".format(names[x])].columns))

data = {}
for x in range(0, len(names)):
    data["data{}".format(names[x])] = d["data{}".format(names[x])].iloc[0:min(h), 0:min(l)]

v = np.stack([data["data{}".format(x)] for x in names])
print("The format of the tensor is: ", v.shape)
v = v.astype(float)
tensor = tl.tensor(v)
rank = int(input("Input the rank: "))
(weight, factors), errors = parafac(tensor, rank=rank, return_errors=True)
print("PARAFAC can explain: ",100*(1 - errors[-1]), "% of the data")
print("New form: ",[f.shape for f in factors])
PARAFAC = {}
for f in range(0,3):
    PARAFAC["data{}".format(f)] = pd.DataFrame(data = factors[f],
                                                    columns = ["component{}".format(f+1) for f in range(0, rank)])
for i in range(0,len(names)):
    if names[i].endswith('.xlsx'):
        names[i] = names[i][:-5]
data = pd.concat([PARAFAC["data0"],  pd.Series(names).rename('Samples')] ,axis=1)
print("\n The sheet is: \n ",data)

if rank == 3:
    plot = str(input("Plot? [y,n]"))
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    if plot == 'y':
        for i in range(0, len(data)):
            if "A" in data["Samples"][i]: ###ATENTION!!!
                ax.scatter(data["component1"][i],data["component2"][i],data["component3"][i], label = data["Samples"][i])#, c = "orange")
            else:
                ax.scatter(data["component1"][i],data["component2"][i],data["component3"][i], label=data["Samples"][i])#, c="m")
        ax.set_title("PARAFAC - 3 Components")
        ax.set_xlabel("Component 1")
        ax.set_ylabel("Component 2")
        ax.set_zlabel("Component 3")
        ax.legend()
        ax.grid()
        plt.show()
        print("Done!")
    else:
        data.to_excel("PARAFAC_{}components.xlsx".format(rank))
        print("The file was saved with {}".format(rank), "Components")
elif rank == 2:
    plot = str(input("Plot? [y,n]"))
    if plot == "y":
        for i in range(0, len(data)):
            if "A" in data["Samples"][i]:
                plt.scatter(data["component1"][i], data["component2"][i], label = data["Samples"][i])#, c = "k")
            else:
                plt.scatter(data["component1"][i], data["component2"][i], label=data["Samples"][i])#, c="g")
        plt.title("PARAFAC - 2 Components")
        plt.xlabel("Component 1")
        plt.ylabel("Component 2")
        plt.legend()
        plt.grid()
        plt.show()
        print("Done!")
    else:
        data.to_excel("PARAFAC_{}components.xlsx".format(rank))
        print("The file was saved with {}".format(rank), "Components")
else:
    data.to_excel("PARAFAC_{}components.xlsx".format(rank))
    print("The file was saved with {}".format(rank), "Components")

##fig, ax = model.biplot(n_feat=4)

"""data1 = pd.concat([PARAFAC["data1"],  pd.Series(names).rename('Samples')] ,axis=1)
data2 = pd.concat([PARAFAC["data2"],  pd.Series(names).rename('Samples')] ,axis=1)

data1.to_excel("PARAFAC_Loading1({}).xlsx".format(data1.shape))
data2.to_excel("PARAFAC_Loading2({}).xlsx".format(data2.shape))"""






"""targett = pd.Series([
    "Amido",
    "Amido",
    "Amido",
    "Liga Neutra",
    "Liga Neutra"
])
con = pd.concat([PARAFAC["data0"], targett], axis=1)
fig = plt.figure()
ax = fig.add_subplot(111)
targets = ['Amido', 'Liga Neutra']
colors = ['g', 'r']
for target, color in zip(targets,colors):
    indicesToKeep = con[0] == target
    ax.scatter(con.loc[indicesToKeep, 'component0']
               , con.loc[indicesToKeep, 'component1']
               , c = color
               , s = 50)
ax.legend(targets, loc ='best')
ax.set_title("PARAFAC - 2 Components", fontsize = 14)
ax.set_xlabel('x - Component 1', fontsize = 12)
ax.set_ylabel("y - Component 1", fontsize = 12)
ax.grid()
plt.show()"""