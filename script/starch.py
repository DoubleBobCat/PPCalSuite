import pandas as pd
import parallel_calculate as pc
import sys

source_file_path = '..\\sourse_data\\source_starch.csv'
result_file_path = '..\\result_data\\result_starch.xlsx'

# Read
try:
    source_df = pd.read_csv(source_file_path)
except FileNotFoundError:
    print(f"Can`t find {source_file_path}")
    sys.exit()
except Exception as e:
    print(f"READ ERROR: {e}")
    sys.exit()

# calculate
calculate_df = pd.DataFrame()
calculate_df['name'] = [name[0] for name in zip(source_df['name'])]
calculate_df['calculate'] = [a1*90/((end-begin)*m/v*1000) for m, begin, end, a1, v in zip(
    source_df['m'], source_df['begin'], source_df['end'], source_df['a1'], source_df['v'])]
calculate_df = calculate_df[['name', 'calculate']]
calculate_df = calculate_df[calculate_df['calculate'] != '']
print("Calculate Data Done.")

# result
result_df = pc.get_df_result(calculate_df, 'starch')

with pd.ExcelWriter(result_file_path, engine='openpyxl') as writer:
    result_df.to_excel(writer, sheet_name='result', index=False)
    source_df.to_excel(writer, sheet_name='source', index=False)
    calculate_df.to_excel(writer, sheet_name='calculate', index=False)
    print("Export Data Done.")
