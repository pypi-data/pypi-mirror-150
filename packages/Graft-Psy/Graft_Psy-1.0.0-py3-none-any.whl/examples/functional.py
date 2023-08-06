from src.basic import Linear, Absolute

lin = Linear(2, 3)
absolute = Absolute(lin)

print(absolute)

for i in range(-10, 10):
    print(absolute(i))