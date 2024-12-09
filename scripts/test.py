import requests
import os
import time
import json

def run_query(dir_, trial):
    cacert = "workspace/sandbox_common/service_cert.pem"
    cert = "workspace/sandbox_common/user0_cert.pem"
    key = "workspace/sandbox_common/user0_privk.pem"

    headers = {'Content-Type': 'application/json'}

    url = 'https://127.0.0.1:8000/app/log/query'
    data = {"query": "query1"}

    s = requests.Session()
    start = time.time()
    r = s.post(url, 
            verify=cacert, 
            cert=(cert,key),
            headers=headers,
            data=json.dumps(data).encode(),
            )

    end = time.time() - start
    print(f"Trial {trial}: {end} seconds")
    with open(f"{dir_}_query_times.csv", 'a') as fp:
        fp.write(f"{end}\n")
    ret = r.json()
    if "error" in ret:
        print(ret)
    # else:
    #     vals = [int(x) for x in json.loads(ret["results"])]
    #     vals.sort()
    #     with open(f"{dir_}/ccf_qry_out.csv", 'w') as f:
    #         for val in vals:
    #             f.write(f"{val}\n")


def load_all_data(dir_, num_batches):
    cacert = "workspace/sandbox_common/service_cert.pem"
    cert = "workspace/sandbox_common/user0_cert.pem"
    key = "workspace/sandbox_common/user0_privk.pem"

    headers = {'Content-Type': 'application/json'}
    url = 'https://127.0.0.1:8000/app/log/insert'

    f = open(f'{dir_}/orders1.csv')
    lines = f.readlines()
    table1 = []

    for line in lines: 
        vals = line.split(",")
        table1.append(vals)
    f.close()
    del lines

    print(f"{len(table1)} rows in Table 1")
    ranges = int(len(table1) / num_batches)
    start_load_time = time.time()
    for i in range(num_batches):
        start = ranges * i
        end = ranges * (i + 1)
        batch_list = table1[start: end]
        batch = {str(start + j): batch_list[j] for j in range(len(batch_list))}

        data = {"table": "orders1", 
                "values": batch
                }


        start = time.time()
        r = requests.post(url, 
                verify=cacert, 
                cert=(cert,key),
                headers=headers,
                data=json.dumps(data).encode(),
                )

        ret = r.json()
        if ret != True:
            print(ret)
    load_time1 = time.time() - start_load_time
    print(f"Table 1 loaded in {load_time1} seconds")
    del table1

    f = open(f'{dir_}/orders2.csv')
    lines = f.readlines()
    table2 = []
    for line in lines: 
        vals = line.split(",")
        table2.append(vals)
    f.close()

    print(f"{len(table2)} rows in Table 2")
    ranges = int(len(table2) / num_batches)
    start_load_time = time.time()
    for i in range(num_batches):
        start = ranges * i
        end = ranges * (i + 1)
        batch_list = table2[start: end]
        batch = {str(start + j): batch_list[j] for j in range(len(batch_list))}

        data = {"table": "orders2", 
                "values": batch
                }


        r = requests.post(url, 
                verify=cacert, 
                cert=(cert,key),
                headers=headers,
                data=json.dumps(data).encode(),
                )

        ret = r.json()
        if ret != True:
            print(ret)
    load_time2 = time.time() - start_load_time
    print(f"Table 2 loaded in {load_time2} seconds")
    with open(f"{dir_}_load_time.csv", 'a') as fp:
        lt = load_time1 + load_time2
        fp.write(f"{lt}")

if __name__ == '__main__':
    # load_partial_data(real_data=True, size=200)
    dir_ = "100MB"
    num_batches = 1000
    load_all_data(dir_, num_batches)
    for i in range(10):
        try:
            run_query(dir_, i)
        except:
            continue
