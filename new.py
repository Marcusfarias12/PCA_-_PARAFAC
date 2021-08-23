import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorly as tl
from tensorly.decomposition import parafac
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.decomposition import PCA
import os

def csv_to_excel(path, path_2_save):

    files = []
    for fname in os.listdir(path):
        if fname.endswith(".csv"):
            files.append(fname)

    print("\n The files are: \n")
    for i in range(0, len(files)):
        print("File {}:".format(i),files[i])

    number = int(input("\nHow many files to convert? "))

    names = []
    for i in range(0,number):
      w = int(input("Input the number of the file you want: "))
      names.append(files[w])

    for i in range(0, len(names)):
        if names[i].endswith('.csv'):
            names[i] = names[i][:-4]


    d = {}
    l = []
    for x in range(0, len(names)):
        d["data{}".format(names[x])] = pd.read_csv(path+'\{}.csv'.format(names[x]),  sep =';', skiprows=2 , decimal=',' )
        d["data{}".format(names[x])] = pd.DataFrame(data = d["data{}".format(names[x])].dropna().values)
        d["data{}".format(names[x])] = d["data{}".format(names[x])].apply(pd.to_numeric, errors='coerce')
        l.append(len(d["data{}".format(names[x])]))
        d["data{}".format(names[x])].to_excel(path_2_save + '\{}.xlsx'.format(names[x]))
        d["data{}".format(names[x])] = pd.read_excel(path_2_save + '\{}.xlsx'.format(names[x]), engine='openpyxl')

    return print("Done!")

