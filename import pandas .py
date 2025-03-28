import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from mpl_toolkits.mplot3d import Axes3D

# 读取 Excel 文件
file_path = r"C:\big-mac-project\BIG-MAC\big-mac-16~25.xlsx"
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
df_all["Year"] = df_all["Year"].str.extract(r"(\d{4})").dropna().astype(int)

# 选取数据较全的前20个国家
top_countries = df_all.groupby("iso_a3").count()["dollar_price"].nlargest(20).index
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

# 生成 20 種依照色環排列的顏色（降低飽和度以減少鮮豔感）
num_colors = len(countries)
H = np.linspace(0, 1, num_colors, endpoint=False)  # 依色環等距分布
S = np.full(num_colors, 0.5)  # 飽和度降低到 0.5
V = np.full(num_colors, 0.8)  # 亮度設定為 0.8
hsv_colors = np.stack([H, S, V], axis=1)
rgb_colors = hsv_to_rgb(hsv_colors)  # 轉換為 RGB 顏色

# 绘制3D柱状图
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection="3d")

dx = dy = 0.8

for i, country in enumerate(countries):
    country_data = df_filtered[df_filtered["iso_a3"] == country]
    x_vals = [year_idx[year] for year in country_data["Year"]]
    y_vals = [i] * len(x_vals)
    z_vals = np.zeros_like(x_vals)
    z_heights = country_data["dollar_price"].values
    ax.bar3d(x_vals, y_vals, z_vals, dx, dy, z_heights, color=rgb_colors[i], edgecolor='black')

# 设置轴标签
ax.set_xticks(range(len(years)))
ax.set_xticklabels(years, ha='right', fontsize=7)
ax.set_yticks(range(len(countries)))
ax.set_yticklabels(countries, fontsize=7, rotation=45)
ax.set_xlabel("Year")
ax.set_ylabel("Country")
ax.set_zlabel("Dollar Price")

# 调整视角
ax.view_init(elev=30, azim=-60)

plt.title("3D Bar Chart of Dollar Price Over Years")
plt.show()