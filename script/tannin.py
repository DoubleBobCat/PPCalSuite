import pandas as pd
import parallel_calculate as pc
import sys

source_filea_path = '..\\sourse_data\\source_tannin.csv'
source_fileb_path = '..\\result_temp.csv'
result_file_path = '..\\result_data\\result_tannin.xlsx'

# Read
try:
    sourcea_df = pd.read_csv(source_filea_path)
except FileNotFoundError:
    print(f"Can`t find {source_filea_path}")
    sys.exit()
except Exception as e:
    print(f"READ ERROR: {e}")
    sys.exit()
try:
    sourceb_df = pd.read_csv(source_fileb_path)
except FileNotFoundError:
    print(f"Can`t find {source_fileb_path}")
    sys.exit()
except Exception as e:
    print(f"READ ERROR: {e}")
    sys.exit()

# calculate


def calculate_tannin_unit(name, sc_a, sc_b, m, a525_1, a525_2):
    temp_c = (a525_2-a525_1)*sc_a+sc_b
    temp_water = 0
    if not sourceb_df.loc[sourceb_df['name'] == name].empty:
        temp = sourceb_df.loc[sourceb_df['name'] == name, 'water'].values[0]
        if temp == temp:
            temp_water = temp
        else:
            temp_water = 0
    if temp_water != 0:
        temp_res = 2*temp_c/m*(1/(1-(temp_water/100)))
        return temp_res
    else:
        return -1


calculate_df = pd.DataFrame()
calculate_df['name'] = [name[0] for name in zip(sourcea_df['name'])]
calculate_df['calculate'] = [calculate_tannin_unit(name, 0.7149, -0.133, m, a525_1, a525_2) for
                             name, m, a525_1, a525_2 in zip(sourcea_df['name'], sourcea_df['m'], sourcea_df['A525_1'], sourcea_df['A525_2'])]
calculate_df = calculate_df[['name', 'calculate']]
calculate_df = calculate_df[calculate_df['calculate'] != '']
print("Calculate Data Done.")

# result
result_df = pc.get_df_result(calculate_df, 'tannin')

with pd.ExcelWriter(result_file_path, engine='openpyxl') as writer:
    result_df.to_excel(writer, sheet_name='result', index=False)
    sourcea_df.to_excel(writer, sheet_name='source', index=False)
    calculate_df.to_excel(writer, sheet_name='calculate', index=False)
    print("Export Data Done.")
