import pandas as pd
import parallel_calculate as pc
import sys

source_file_path = '..\\sourse_data\\source_amylose.csv'
result_file_path = '..\\result_data\\result_amylose.xlsx'

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
calculate_df['calculate'] = [
    ((a720*0.862)-0.0017)*100 for m0, a720 in zip(source_df['m0'], source_df['A720'])]
calculate_df = calculate_df[['name', 'calculate']]
calculate_df = calculate_df[calculate_df['calculate'] != '']
print("Calculate Data Done.")

# result
result_df = pc.get_df_result(calculate_df, 'amylose')

with pd.ExcelWriter(result_file_path, engine='openpyxl') as writer:
    result_df.to_excel(writer, sheet_name='result', index=False)
    source_df.to_excel(writer, sheet_name='source', index=False)
    calculate_df.to_excel(writer, sheet_name='calculate', index=False)
    print("Export Data Done.")
