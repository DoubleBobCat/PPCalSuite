import ctypes

# 加载DLL
lib = ctypes.CDLL(r"D:\School\liquor\script\model\parallel_calculate.dll")

# 设置参数类型
lib.parallel_calculate_c.argtypes = [
    ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]
lib.parallel_calculate_c.restype = ctypes.c_double

# 准备数据
# numbers = [
#     47.46110436,
#     53.80491533,
#     50.08568155,
#     33.75339409,
#     93.69476636,
#     53.33081466,
#     52.61656268,
#     50.58416327,
#     51.46772944,
#     55.33384996,
#     76.00199214,
#     76.96404267,
#     67.55732634,
#     75.52993007,
#     76.47999209
# ]
numbers = [1, 5, 9]
numbers_array = (ctypes.c_double * len(numbers))(*numbers)

# 调用函数
result = lib.parallel_calculate_c(numbers_array, len(numbers))

# 输出结果
print(result)
