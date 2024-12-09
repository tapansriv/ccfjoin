import duckdb


dirs = ["1MB", "10MB", "100MB", "1GB", "10GB"]

for dir_ in dirs:
    tbl1 = f"{dir_}/orders1.csv"
    tbl2 = f"{dir_}/orders2.csv"

    qry = f'''
    SELECT DISTINCT tbl1.column1 
    FROM '{tbl1}' as tbl1 JOIN '{tbl2}' as tbl2 ON tbl1.column1 = tbl2.column1
    ORDER BY tbl1.column1;
    '''

    ret = duckdb.sql(qry)
    results = ret.fetchall()

    f = open(f"{dir_}/ground_truth.csv", 'w')
    for r in results:
        x = r[0]
        f.write(f"{x}\n")

