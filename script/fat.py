import pandas as pd
import parallel_calculate as pc
import sys

source_file_path = '..\\sourse_data\\source_fat.csv'
result_file_path = '..\\result_data\\result_fat.xlsx'

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
check_df['m0_check'] = ['YES' if round(abs(
    m0 - m0_hot), 4) <= 0.002 else 'NO' for m0, m0_hot in zip(source_df['m0'], source_df['m0_hot'])]
check_df['m1_check'] = ['YES' if round(abs(
    m1 - m1_hot), 4) <= 0.002 else 'NO' for m1, m1_hot in zip(source_df['m1'], source_df['m1_hot'])]
check_df = check_df[['name', 'm0_check', 'm1_check']]
print("Check Data Done.")

# calculate
calculate_df = pd.DataFrame()
calculate_df['name'] = [name[0] for name in zip(source_df['name'])]
calculate_df['calculate'] = [round((m1-m0)/m2*100, 6) if (m0_check == 'YES' and m1_check == 'YES') else '' for m0, m1, m2, m0_check,
                             m1_check in zip(source_df['m0_hot'], source_df['m1_hot'], source_df['m2'], check_df['m0_check'], check_df['m1_check'])]
calculate_df = calculate_df[['name', 'calculate']]
calculate_df = calculate_df[calculate_df['calculate'] != '']
print("Calculate Data Done.")

# result
result_df = pc.get_df_result(calculate_df, 'fat')

with pd.ExcelWriter(result_file_path, engine='openpyxl') as writer:
    result_df.to_excel(writer, sheet_name='result', index=False)
    source_df.to_excel(writer, sheet_name='source', index=False)
    check_df.to_excel(writer, sheet_name='check', index=False)
    calculate_df.to_excel(writer, sheet_name='calculate', index=False)
    print("Export Data Done.")
