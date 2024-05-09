def a(val, p=[]):
    p.append(val)
    return p

for v in a(1):
    print(v)

print("---")

for v in a(2):
    print(v)