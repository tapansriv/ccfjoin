f = open("out")
lines = f.readlines()
f.close()
ret = []
for line in lines:
    x = int(line.strip())
    ret.append(x)
ret.sort()

with open("out2", 'w') as fp:
    for val in ret:
        fp.write(f"{val}\n")
