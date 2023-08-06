from src.basic import Polynomial

poly = Polynomial([(1, 2), (3, 1), (2, 0)], 3)

print(poly)

for i in range(15):
    print(poly(i))