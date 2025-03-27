import pandas as pd
import matplotlib.pyplot as plt
BM_data=pd.read_csv("output-data/big-mac-2025-01-01.xls")  
print(BM_data)
x=BM_data['Country']
y=BM_data['local_price']