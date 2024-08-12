v = [float]*6
pre_add_v = [float]*4
res = 0.0
for i in range(6):
    v[i] = float(input(f'input v{i}: '))
for i in range(4):
    pre_add_v[i] = float(input(f'input pre add v{i}: '))
for i in range(5):
    if i > 0:
        res += (v[i+1]-v[i]+pre_add_v[i-1])
    else:
        res += (v[i+1]-v[i])
res /= 5
print("ans=", res)
