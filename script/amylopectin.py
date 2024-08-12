import pandas as pd
import parallel_calculate as pc
import sys

source_file_path = '..\\result_temp.csv'
result_file_path = '..\\result_data\\result_amylopectin.xlsx'

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
check_df['amylose_check'] = ['YES' if amylose !=
                             '' else 'NO' for amylose in zip(source_df['amylose'])]
check_df = check_df[['name', 'amylose_check']]
print("Check Data Done.")

# calculate
calculate_df = pd.DataFrame()
calculate_df['name'] = [name[0] for name in zip(source_df['name'])]
calculate_df['calculate'] = [(100-amylose) if amylose_check == 'YES' else '' for amylose,
                             amylose_check in zip(source_df['amylose'], check_df['amylose_check'])]
calculate_df = calculate_df[['name', 'calculate']]
calculate_df = calculate_df[calculate_df['calculate'] != '']
print("Calculate Data Done.")

# result
result_df = pd.DataFrame()
result_df['name'] = [name[0] for name in zip(calculate_df['name'])]
result_df['amylopectin'] = [calculate[0]
                            for calculate in zip(calculate_df['calculate'])]
print("Result Data Done.")

with pd.ExcelWriter(result_file_path, engine='openpyxl') as writer:
    result_df.to_excel(writer, sheet_name='result', index=False)
    source_df.to_excel(writer, sheet_name='source', index=False)
    check_df.to_excel(writer, sheet_name='check', index=False)
    calculate_df.to_excel(writer, sheet_name='calculate', index=False)
    print("Export Data Done.")
