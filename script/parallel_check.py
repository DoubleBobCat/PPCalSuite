import parallel_calculate as pc
temp = 0.00
swap = []
flag = True
while flag:
    temp = input()
    if temp != 'q':
        temp = float(temp)
        if temp > 0:
            swap.append(temp)
            len_swap = len(swap)
            for i in range(len_swap):
                for j in range(len_swap):
                    if j > i:
                        if pc.parallel_check(swap[i], swap[j]):
                            print(i, j, "pass")
                        else:
                            print(i, j, "NoPass")
        else:
            print("???")
            flag = False
    else:
        flag = False
