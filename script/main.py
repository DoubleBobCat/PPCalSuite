import pandas as pd
from PIL import Image
import os
# Pre command
os.system('cls')

# Calculate Period A
print("/****** Calculate Period A ******/")
print("-> water")
os.system('python water.py')
print("-> starch")
os.system('python starch.py')
print("-> amylose")
os.system('python amylose.py')
print("-> protein")
os.system('python protein.py')
print("-> fat")
os.system('python fat.py')

# Rollup Period A
print("\n/****** Rollup Period A ******/")
files_A = [
    "../result_data/result_water.xlsx",
    "../result_data/result_starch.xlsx",
    "../result_data/result_amylose.xlsx",
    "../result_data/result_protein.xlsx",
    "../result_data/result_fat.xlsx"
]
result_temp_df = pd.DataFrame()
for file in files_A:
    df = pd.read_excel(file, sheet_name=0)
    result_type = file.split('_')[2].split('.')[0]
    if 'name' in df.columns:
        df.set_index('name', inplace=True)
        result_temp_df = pd.merge(result_temp_df, df, left_index=True,
                                  right_index=True, how='outer')
print("Result Temp Data Done.")
result_temp_df.to_csv("../result_temp.csv", index=True, encoding='utf-8-sig')
print("Export Data Done.")

# Calculate Period B
print("\n/****** Calculate Period B ******/")
print("-> amylopectin")
os.system('python amylopectin.py')
print("-> tannin")
os.system('python tannin.py')

# Rollup Period B
print("\n/****** Rollup Period B ******/")
files_B = [
    "../result_data/result_water.xlsx",
    "../result_data/result_starch.xlsx",
    "../result_data/result_amylose.xlsx",
    "../result_data/result_amylopectin.xlsx",
    "../result_data/result_protein.xlsx",
    "../result_data/result_fat.xlsx",
    "../result_data/result_tannin.xlsx"
]
result_df = pd.DataFrame()
for file in files_B:
    df = pd.read_excel(file, sheet_name=0)
    result_type = file.split('_')[2].split('.')[0]
    if 'name' in df.columns:
        df.set_index('name', inplace=True)
        result_df = pd.merge(result_df, df, left_index=True,
                             right_index=True, how='outer')
print("Result Data Done.")
result_df.to_csv("../result.csv", index=True, encoding='utf-8-sig')
os.remove("../result_temp.csv")
print("Export Data Done.")

# show data
print("\n/****** Show Data ******/")
result_df_ff = pd.read_csv('../result.csv')
show_df = pd.DataFrame()
show_df['name'] = [name[0] for name in zip(result_df_ff['name'])]
show_df['water'] = [((str(round(water, 2)) + '%') if water != -1 else '')
                    if pd.notna(water) else '' for water in result_df_ff['water']]
show_df['starch'] = [((str(round(starch, 2)) + '%') if starch > 65 else ('-' + str(
    round(starch, 2)) + '%')) if pd.notna(starch) else '' for starch in result_df_ff['starch']]
show_df['amylose'] = [((str(round(amylose, 2)) + '%') if amylose != -1 else '')
                      if pd.notna(amylose) else '' for amylose in result_df_ff['amylose']]
show_df['amylopectin'] = [((str(round(amylopectin, 2)) + '%') if amylopectin < 100 else '')
                          if pd.notna(amylopectin) else '' for amylopectin in result_df_ff['amylopectin']]
show_df['protein'] = [((str(round(protein, 2)) + '%') if protein != -1 else '')
                      if pd.notna(protein) else '' for protein in result_df_ff['protein']]
show_df['fat'] = [((str(round(fat, 2)) + '%') if fat != -1 else '')
                  if pd.notna(fat) else '' for fat in result_df_ff['fat']]
show_df['tannin'] = [((str(round(tannin, 2)) + '%') if tannin != -1 else 'Want:Water')
                     if pd.notna(tannin) else '' for tannin in result_df_ff['tannin']]
show_df = show_df[['name', 'water', 'starch',
                   'amylose', 'amylopectin', 'protein', 'fat', 'tannin']]
print("Show Data Done.")
show_df.to_csv('../data.csv', index=False, encoding='utf-8-sig')
print("Export Data Done.")
