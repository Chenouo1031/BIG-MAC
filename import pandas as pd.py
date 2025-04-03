import pandas as pd #載入pandas資料處理庫
import numpy as np  #載入numpy數值計算庫
import matplotlib.pyplot as plt #載入matplotlib繪圖庫
import seaborn as sns   #載入seaborn視覺化庫
from mpl_toolkits.mplot3d import Axes3D #載入3D繪圖庫

# 讀取 Excel 文件
file_path = r"C:/big-mac-project/BIG-MAC/big-mac-16~25.xlsx"    #設定檔案路徑
xls = pd.ExcelFile(file_path)  #加載Excel資料表 

# 利用for迴圈收集所有年份的數據
data_list = []  #建立空的列表
for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)   #讀取Excel資料表
    df["Year"] = sheet  #新增年份信息
    data_list.append(df[["iso_a3", "dollar_price", "Year"]])   #新增數據 

# 合併數據
df_all = pd.concat(data_list, ignore_index=True)    #合併2維data_list陣列

# 處理年份格式（提取年份）
df_all["Year"] = df_all["Year"].str.extract(r"(\d{4})").dropna().astype(int)    #提取4位數的年份並轉成int格式

# 選取前20個國家
top_countries = df_all.groupby("iso_a3").count()["dollar_price"].nlargest(20).index  #篩選擁有最多有效數據的前20個國家
df_filtered = df_all[df_all["iso_a3"].isin(top_countries)]  #提取前20個國家的數據

# 取得唯一國家和年份
countries = df_filtered["iso_a3"].unique()  #提取國家簡稱(不重複)
years = sorted(df_filtered["Year"].unique())    #提取年份(不重複)並按順序排列

# 建立資料矩陣
country_idx = {country: i for i, country in enumerate(countries)}   #為國家簡稱建立索引字典並賦予索引值
year_idx = {year: i for i, year in enumerate(years)}    #為年份建立索引字典並賦予索引值

#建立座標網格
X, Y = np.meshgrid(range(len(years)), range(len(countries)))    #建立x,y座標的索引矩陣
Z = np.zeros_like(X, dtype=float)   #建立z座標的陣列，大小和x軸相同，資料型態為浮點數

#存儲表格數值
for row in df_filtered.itertuples():    #利用for迴圈和itertuples瀏覽表格數據
    i, j = country_idx[row.iso_a3], year_idx[row.Year]  # 利用row.iso_a3和row.Year取x,y的值
    Z[i, j] = row.dollar_price     #利用row.dollar_price取z的值

# 設定顏色
bar_colors = plt.cm.turbo(np.linspace(0.3, 0.8, len(countries)))  #使用turbo內建顏色來顯示圖表

# 繪製3D長條圖
fig = plt.figure(figsize=(12, 10))  #設定圖表大小
ax = fig.add_subplot(111, projection="3d")  #繪製3D柱狀圖

# 繪製長條圖
dx = dy = 0.8   #設定柱子寬度

#指定數值
for i, country in enumerate(countries):       #利用enumerate函式同時瀏覽和抓取資料
    country_data = df_filtered[df_filtered["iso_a3"] == country]    #篩選所需的國家資料
    x_vals = [year_idx[year] for year in country_data["Year"]]  #指定x軸數值
    y_vals = [i] * len(x_vals)  #指定y軸數值
    z_vals = np.zeros_like(x_vals)  #初始化z座標
    z_heights = country_data["dollar_price"].values     #指定z軸數值
    ax.bar3d(x_vals, y_vals, z_vals, dx, dy, z_heights, color=bar_colors[i], edgecolor='black')     #繪製3D圖表

# 設定軸標籤，設定字體大小和角度使其不擠在一塊
ax.set_xticks(range(len(years)))    #設定x軸刻度
ax.set_xticklabels(years, ha='right', fontsize=7)   #設定x軸刻度數值
ax.set_yticks(range(len(countries)))    #設定y軸刻度
ax.set_yticklabels(countries, fontsize=6, rotation=285)     #設定y軸刻度數值
ax.set_xlabel("Year")   #設定x軸標題為年份
ax.set_ylabel("Country")    #設定y軸標題為國家
ax.set_zlabel("Dollar Price")   #設定z軸標題為美金

# 調整視角
ax.view_init(elev=30, azim=-60)     #調整3D圖的仰角和水平角度

plt.title("3D Bar Chart of Dollar Price Over Years")    #設定圖表標題
plt.show()      #展示圖表
