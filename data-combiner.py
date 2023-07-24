import pandas as pd
import os

folder_path = 'data/'
files = os.listdir(folder_path)

pands = []

try:
    for file in files:
        df = pd.read_csv(folder_path + file)
        df['Job'] = file[:-4]
        pands.append(df)
except Exception as e:
    print(f'Error: {e}! in file: {file}')

combined_df = pd.concat(pands, ignore_index=True)

combined_df.to_csv('results.csv')

print(combined_df.head())
print('Success!')