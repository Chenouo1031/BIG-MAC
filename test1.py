import pandas as pd
import matplotlib.pyplot as plt
BM_data=pd.read_csv("output-data/2025.csv")  
print(BM_data)
x=BM_data['Country']
y=BM_data['dollar_price']
plt.xlabel("Country")
plt.ylabel("dollar_price")
plt.plot(x,y)
plt.show()