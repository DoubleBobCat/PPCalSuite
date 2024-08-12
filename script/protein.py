import pandas as pd
import parallel_calculate as pc
import sys

source_file_path = '..\\sourse_data\\source_protein.csv'
result_file_path = '..\\result_data\\result_protein.xlsx'

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
calculate_df['calculate'] = [d_per[0] for d_per in zip(source_df['d_per'])]
calculate_df = calculate_df[['name', 'calculate']]
calculate_df = calculate_df[calculate_df['calculate'] != '']
print("Calculate Data Done.")

# result
result_df = pc.get_df_result(calculate_df, 'protein')

with pd.ExcelWriter(result_file_path, engine='openpyxl') as writer:
    result_df.to_excel(writer, sheet_name='result', index=False)
    source_df.to_excel(writer, sheet_name='source', index=False)
    calculate_df.to_excel(writer, sheet_name='calculate', index=False)
    print("Export Data Done.")
