import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from mpl_toolkits.mplot3d import Axes3D

df=pd.read_csv("output-data/2025.csv") 

file_path = "c:/big-mac-project/BIG-MAC/output-data/2025.xlsx"  # 確保檔案路徑正確
xls = pd.ExcelFile(file_path)

# 讀取 2025 年 1 月的數據
df_2025 = pd.read_excel(xls, sheet_name="Jan2025")

# 選擇需要的欄位，並移除缺失值
df_plot = df_2025[['iso_a3', 'dollar_valuation']].dropna()

# 設定圖形大小
plt.figure(figsize=(12, 6))

# 生成漸層顏色
norm = plt.Normalize(df_plot['dollar_valuation'].min(), df_plot['dollar_valuation'].max())
sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=norm)
colors = [sm.to_rgba(val) for val in df_plot['dollar_valuation']]

# 使用 Seaborn 繪製長條圖
barplot = sns.barplot(data=df_plot, x='iso_a3', y='dollar_valuation', color='gray')

# 設定每個長條的顏色
for bar, color in zip(barplot.patches, colors):
    bar.set_facecolor(color)

# 設定標題和標籤
plt.title("Dollar Valuation by Country (Jan 2025)", fontsize=14)
plt.xlabel("Country (ISO A3)", fontsize=12)
plt.ylabel("Dollar Valuation", fontsize=12)
plt.xticks(rotation=90)  # 旋轉 X 軸標籤以便閱讀

fig = plt.gcf()  # 獲取當前圖形
cbar = fig.colorbar(sm, ax=plt.gca())  
cbar.set_label("Dollar Valuation")

# 顯示圖表
plt.show()