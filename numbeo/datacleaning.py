import pandas as pd
import numpy as np
import sqlite3

df = pd.read_excel('numbeo/cost_of_global(in TWD).xlsx')
old_columns = df.columns.tolist()

new_columns = old_columns[1:]
df = df[new_columns]
print(len(df))
#將表格內所有?替換為空字串
df = df.replace('?', np.nan)
df = df.dropna(how='any', axis=0)
print(len(df))
#df.to_excel('./cost_of_global(in TWD_cleaned).xlsx', index=False)
#將表格轉乘sqlite3資料庫
conn = sqlite3.connect('numbeo/cost_of_global.db')
df.to_sql('cost_of_global', conn, if_exists='replace', index=False)
conn.close()