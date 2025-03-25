import cv2
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import pyreadstat

# quatraiset of Hastie's "quadratic model"
df, meta = pyreadstat.read_sas7bdat(r"C:\Users\adayc\Desktop\code\Drug\DA_data\new_data\diabetes2.sas7bdat")
print(df.head())  
print(meta.column_names)  
print(meta.column_labels)  

# original data
dftxt = pd.read_csv(r"C:\Users\adayc\Desktop\code\Drug\DA_data\new_data\diabetesrwrite1.txt", sep="\s+")
num_rows, num_columns = dftxt.shape
print(dftxt.head())
print(f"rows: {num_rows}")
print(f"columns: {num_columns}")

# check the space seperation
# with open(r"C:\Users\adayc\Desktop\code\Drug\DA_data\diabetesrwrite1.txt", "r", encoding="utf-8") as f:
#     first_line = f.readline()
#     print(repr(first_line)) 