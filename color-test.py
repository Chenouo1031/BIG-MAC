import pandas as pd  #載入pandas資料處理庫
import numpy as np #載入numpy數值計算庫
import matplotlib.pyplot as plt #載入matplotlib繪圖庫
import seaborn as sns #載入seaborn視覺化庫
from mpl_toolkits.mplot3d import Axes3D #載入3D繪圖庫

# 讀取 Excel 文件
file_path = "c:/big-mac-project/BIG-MAC/2025x20.xlsx"  # 確保檔案路徑正確
xls = pd.ExcelFile(file_path)   #加載Excel資料表
df_2025 = pd.read_excel(xls, sheet_name="Jan2025")  #讀取Excel資料表

# 選擇需要的欄位，並移除缺失值
df_plot = df_2025[['iso_a3', 'dollar_valuation']].dropna()  #篩選所需數值

# 設定圖形大小
plt.figure(figsize=(12, 6))   #設定圖表大小

# 生成漸層顏色
norm = plt.Normalize(df_plot['dollar_valuation'].min(), df_plot['dollar_valuation'].max())  #標準化數值範圍，設定最大值和最小值
sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=norm)  #使用coolwarm顏色來展示圖表
colors = [sm.to_rgba(val) for val in df_plot['dollar_valuation']]   #將數值轉換為對應的顏色

# 使用 Seaborn 繪製長條圖
barplot = sns.barplot(data=df_plot, x='iso_a3', y='dollar_valuation', color='gray') #給定x軸,y軸和顏色繪製長條圖

# 設定每個長條的顏色
for bar, color in zip(barplot.patches, colors):     #配對每個長條與顏色
    bar.set_facecolor(color)    #設定長條的顏色

# 設定標題和標籤
plt.title("Dollar Valuation by Country (Jan 2025)", fontsize=14)    #設定圖表標題
plt.xlabel("Country (ISO A3)", fontsize=12) #設定x軸標籤
plt.ylabel("Dollar Valuation", fontsize=12) #設定y軸標籤
plt.xticks(rotation=90)  # 旋轉 X 軸標籤以便閱讀

#在圖表右側建立顏色條圖例
fig = plt.gcf()  # 獲取當前圖形
cbar = fig.colorbar(sm, ax=plt.gca())   #建立顏色條 
cbar.set_label("Dollar Valuation")  #設定顏色條標籤
# 顯示圖表
plt.show()  #展示圖表