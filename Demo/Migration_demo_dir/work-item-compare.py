import pandas as pd
import numpy as np

df1=pd.read_excel('./Demo/TFS-Workitem.xlsx')
df2=pd.read_excel('./Demo/Ado-Workitem.xlsx')

df1.equals(df2)

comparison_values = df1.values == df2.values
print (comparison_values)

rows,cols=np.where(comparison_values==False)

for item in zip(rows,cols):
    df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]],df2.iloc[item[0], item[1]])

df1.to_excel('./Demo/work_item_validation_result.xlsx',index=False,header=True)