import pandas as pd
import time
import ctypes

lib = ctypes.CDLL('./model/parallel_calculate.dll')
lib.parallel_calculate_c.argtypes = [
    ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]
lib.parallel_calculate_c.restype = ctypes.c_double


def get_parallel_result(_numbers):
    numbers_array = (ctypes.c_double * len(_numbers))(*_numbers)
    result = lib.parallel_calculate_c(numbers_array, len(_numbers))
    return result


def get_df_result(calculate_df, type):
    grouped_data = []
    result_data = []
    for name, group in calculate_df.groupby('name'):
        calculate_list = group['calculate'].tolist()
        grouped_data.append((name, calculate_list))
    for item in grouped_data:
        result = get_parallel_result(item[1])
        result_data.append((item[0], result))
    result_df = pd.DataFrame()
    result_df['name'] = [item[0] for item in result_data]
    result_df[type] = [item[1] for item in result_data]
    print("Result Data Done.")
    return result_df
