import duckdb


dirs = ["1MB", "10MB", "100MB", "1GB", "10GB"]
values = {}
for dir_ in dirs:
    tbl1 = f"{dir_}/orders1.csv"
    tbl2 = f"{dir_}/orders2.csv"

    # qry = f'''
    # SELECT DISTINCT tbl1.column1 
    # FROM '{tbl1}' as tbl1 JOIN '{tbl2}' as tbl2 ON tbl1.column1 = tbl2.column1
    # ORDER BY tbl1.column1;
    # '''
    qry = f'''
    SELECT tbl.column1, COUNT(tbl.column1)
    FROM '{tbl1}' as tbl GROUP BY tbl.column1 ORDER BY tbl.column1
    '''

    ret = duckdb.sql(qry)
    results = ret.fetchall()


    lst = [r[0] for r in results]
    values[dir_] = lst

num_samples = [1, 9, 90, 900, 9000]
final_results = []
for i in range(5):
    n = num_samples[i]

    union = set()
    for j in range(i):
        dir_ = dirs[j] 
        print(f"Union {dir_}")
        cur_vals = set(values[dir_])
        union = union | cur_vals

    intersection = None
    for j in range(i, 5):
        dir_ = dirs[j] 
        print(f"Intersection {dir_}")
        cur_vals = set(values[dir_])
        if intersection is None:
            intersection = cur_vals
        else:
            intersection = intersection & cur_vals
    if i == 0:
        print(intersection)
        print(union)
    to_write = list(intersection - union)[:n]
    assert len(to_write) == n
    assert len([x for x in to_write if x in union]) == 0
    assert len([x for x in to_write if x in intersection]) == n
    final_results.extend(to_write)    

with open("synthetic_db.csv", 'w') as fp:
    for v in final_results:
        fp.write(f"{v}\n")



'''
Output the selectivity of using the synthetic dataset
'''

dirs = ["1MB", "10MB", "100MB", "1GB", "10GB"]

for dir_ in dirs:
    tbl1 = f"{dir_}/orders1.csv"
    tbl2 = "synthetic_db.csv"

    qry = f'''
    SELECT DISTINCT tbl1.column1 
    FROM '{tbl1}' as tbl1 JOIN '{tbl2}' as tbl2 ON tbl1.column1 = tbl2.column0
    ORDER BY tbl1.column1;
    '''

    ret = duckdb.sql(qry)
    results = ret.fetchall()
    print(f"{dir_}: {len(results)}")







