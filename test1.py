import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

BM_data=pd.read_csv("output-data/2025.csv") 

plt.figure(figsize=(30,16))
x=BM_data['iso_a3']
y=BM_data['dollar_price']

plt.xlabel("Country")
plt.ylabel("USD")
plt.bar(x,y)
plt.show()