from src.basic import Linear

lin1 = Linear(2, 0)
lin2 = Linear(3, 2)
lin3 = Linear(-1, 0)

periodic = lin1(ub=5) >> lin2(lb=5, ub=10) >> lin3(lb=10)

print(periodic)

for i in range(15):
    print(periodic(i))