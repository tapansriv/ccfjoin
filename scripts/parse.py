import pandas as pd

dirs = ["10GB"]

for dir_ in dirs:
    f = open(f"{dir_}/orders.tbl")
    lines = f.readlines()
    print(len(lines))
    f.close()

    table1 = []
    table2 = []
    limit = int(len(lines) / 2)
    for i in range(len(lines)):
        line = lines[i]
        vals = line.split("|")
        if i < limit: 
            table1.append(vals[:-1])
        else:
            table2.append(vals[:-1])

    df = pd.DataFrame(table1)
    print(df)
    df.to_csv(f"{dir_}/orders1.csv", index=False, header=False)

    df = pd.DataFrame(table2)
    print(df)
    df.to_csv(f"{dir_}/orders2.csv", index=False, header=False)



