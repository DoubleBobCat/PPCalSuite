import pandas as pd
import parallel_calculate as pc
import sys

source_file_path = '..\\sourse_data\\source_water.csv'
result_file_path = '..\\result_data\\result_water.xlsx'

# Read
try:
    source_df = pd.read_csv(source_file_path)
except FileNotFoundError:
    print(f"Can`t find {source_file_path}")
    sys.exit()
except Exception as e:
    print(f"READ ERROR: {e}")
    sys.exit()

# check
check_df = pd.DataFrame()
check_df['name'] = [name[0] for name in zip(source_df['name'])]
check_df['empty_check'] = ['YES' if round(abs(empty_pre - empty_hot), 4) <= 0.002 else 'NO' for empty_pre,
                           empty_hot in zip(source_df['empty_pre'], source_df['empty_hot'])]
check_df['m1m2'] = ['YES' if abs(add_hot_m1 - add_hot_m2) <= 0.002 else 'NO' for add_hot_m1,
                    add_hot_m2 in zip(source_df['add_hot_m1'], source_df['add_hot_m2'])]
check_df['m2m3'] = ['NO' if add_hot_m3 == '' else ('YES' if abs(
    add_hot_m2 - add_hot_m3) <= 0.002 else 'NO') for add_hot_m2, add_hot_m3 in zip(source_df['add_hot_m2'], source_df['add_hot_m3'])]
check_df = check_df[['name', 'empty_check', 'm1m2', 'm2m3']]
print("Check Data Done.")

# calculate


def cal(a, b, c, d):
    e = (b-c)/(b-a)*100
    f = (b-d)/(b-a)*100
    return (e+f)/2


calculate_df = pd.DataFrame()
calculate_df['name'] = [name[0] for name in zip(source_df['name'])]
calculate_df['calculate'] = [(cal(empty_hot, add, add_hot_m1, add_hot_m2) if m1m2 == 'YES' else (cal(empty_hot, add, add_hot_m2, add_hot_m3) if m2m3 == 'YES' else '')) if empty_check == 'YES' else '' for empty_hot, add, add_hot_m1,
                             add_hot_m2, add_hot_m3, empty_check, m1m2, m2m3 in zip(source_df['empty_hot'], source_df['add'], source_df['add_hot_m1'], source_df['add_hot_m2'], source_df['add_hot_m3'], check_df['empty_check'], check_df['m1m2'], check_df['m2m3'], )]
calculate_df = calculate_df[['name', 'calculate']]
calculate_df = calculate_df[calculate_df['calculate'] != '']
print("Calculate Data Done.")

# result
result_df = pc.get_df_result(calculate_df, 'water')

with pd.ExcelWriter(result_file_path, engine='openpyxl') as writer:
    result_df.to_excel(writer, sheet_name='result', index=False)
    source_df.to_excel(writer, sheet_name='source', index=False)
    check_df.to_excel(writer, sheet_name='check', index=False)
    calculate_df.to_excel(writer, sheet_name='calculate', index=False)
    print("Export Data Done.")
