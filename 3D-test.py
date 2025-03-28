import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_excel("c:/big-mac-project/BIG-MAC/output-data/未命名的試算表.xlsx", engine="openpyxl")
# 读取 Excel 文件
file_path = "c:/big-mac-project/BIG-MAC/output-data/未命名的試算表.xlsx"  # 请替换为你的文件路径
xls = pd.ExcelFile(file_path)

# 收集所有年份的数据
data_list = []
for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    df["Year"] = sheet  # 添加年份信息
    data_list.append(df[["iso_a3", "dollar_price", "Year"]])

# 合并数据
df_all = pd.concat(data_list, ignore_index=True)

# 处理年份格式（提取年份）
df_all["Year"] = df_all["Year"].str.extract("(\d{4})").astype(int)

# 选取前10个国家（避免柱子过多）
top_countries = df_all["iso_a3"].value_counts().index[:10]
df_filtered = df_all[df_all["iso_a3"].isin(top_countries)]

# 获取唯一国家和年份
countries = df_filtered["iso_a3"].unique()
years = sorted(df_filtered["Year"].unique())

# 创建数据矩阵
country_idx = {country: i for i, country in enumerate(countries)}
year_idx = {year: i for i, year in enumerate(years)}

X, Y = np.meshgrid(range(len(years)), range(len(countries)))
Z = np.zeros_like(X, dtype=float)

for _, row in df_filtered.iterrows():
    i, j = country_idx[row["iso_a3"]], year_idx[row["Year"]]
    Z[i, j] = row["dollar_price"]

# 绘制3D柱状图
fig = plt.figure(figsize=(40,40))
ax = fig.add_subplot(111, projection="3d")

# 定義每根柱子的顏色
colors = ['red', 'blue', 'green', 'purple', 'orange', 'yellow']  # 可以自行擴充

# 確保顏色數量與柱子數量一致
colors = colors[:len(X.flatten())]

dx = dy = 0.6  # 柱子宽度
ax.bar3d(X.flatten(), Y.flatten(), np.zeros_like(Z.flatten()), dx, dy, Z.flatten(), shade=True)
ax.bar3d(X.flatten(), Y.flatten(), np.zeros_like(Z.flatten()), dx, dy, Z.flatten(), color='red')


# 设置轴标签
ax.set_xticks(range(len(years)))
ax.set_xticklabels(years, rotation=45)
ax.set_yticks(range(len(countries)))
ax.set_yticklabels(countries)
ax.set_xlabel("Year")
ax.set_ylabel("Country")
ax.set_zlabel("Dollar Price")

plt.title("3D Bar Chart of Dollar Price Over Years")
plt.show()
