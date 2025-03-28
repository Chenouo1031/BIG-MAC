import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

BM_data=pd.read_csv("output-data/2025.csv") 

plt.figure(figsize=(30,16))
x=BM_data['iso_a3']
y=BM_data['dollar_valuation']

# 定義每根柱子的顏色
colors = ['red', 'blue', 'green', 'purple', 'orange', 'yellow']  # 可以自行擴充

# 確保顏色數量與柱子數量一致
colors = colors[:len(x)]  # 若顏色數不足，可以複製 colors * (len(x) // len(colors) + 1)

# 創建 3D 圖


# 繪製 3D 長條圖（每條使用不同顏色）
plt.bar(x, y,  color=colors, edgecolor='black')

plt.xlabel("Country")
plt.ylabel("USD")
plt.bar(x,y)
plt.show()