export function insert_data(request) {
  const tbl1 = "orders1";
  const tbl2 = "orders2";
  // console.log(ccf.kv.has(tbl1));
  // console.log(ccf.kv.has(tbl2));
  // console.log('before');
  let params = request.body.json();
  // console.log(params.values);
  // console.log(Object.keys(params.values));
  // console.log(params.table);
  const tblstr = params.table.toString();
  console.log(tblstr);
  const table = tblstr;

  for (const [key, value] of Object.entries(params.values)) {
    // console.log(`${key}: ${value}`);
    // console.log(typeof value);
    const k2 = ccf.strToBuf(key.toString());
    const v2 = JSON.stringify(value);
    // console.log(v2);
    // console.log(JSON.stringify(value));
    // console.log(ccf.bufToStr(table));
    ccf.kv[table].set(k2, ccf.strToBuf(v2));
    // console.log(ccf.bufToStr(table));
    // const val = ccf.bufToStr(ccf.kv[table].get(k2));
    // console.log(val);
    // const val2 = JSON.parse(val);
    // console.log(val2);
    // console.log(val2[0]);
  }

  // if (table === tbl1) {
  //   console.log(ccf.bufToStr(ccf.kv[tbl1].get(ccf.strToBuf("0"))));
  // } else {
  //   console.log(ccf.bufToStr(ccf.kv[tbl2].get(ccf.strToBuf("0"))));
  // }
  // console.log(typeof ccf.kv[table]);
  return { body: true };
}

function select(rows, index) {
  const results = []
  ccf.kv["join"].forEach(function(value, key, tbl) {
    const row = JSON.parse(ccf.bufToStr(tbl.get(key)));
    // results.push(row[index]);
    const select_val = ccf.strToBuf(row[index].toString());
    ccf.kv["select"].set(key, select_val);
  });
  return results;
}

function hashjoin(table1, index1, table2, index2) {
  const results = [];
  // const k2 = ccf.strToBuf("join");
  // const v2 = JSON.stringify([]);
  // ccf.kv["results"].set(k2, ccf.strToBuf(v2));

  const hashmap = new Map();
  var foo = 0;
  ccf.kv[table1].forEach(function(value, key, tbl1) {
    foo += 1;
    const row = JSON.parse(ccf.bufToStr(tbl1.get(key)));
    const join_val = row[index1];
    if (hashmap.has(join_val)) {
      hashmap.get(join_val).push(row);
    } else {
      const singleton = new Array(row);
      hashmap.set(join_val, singleton);
    }
  });

  console.log(foo);
  var index = 0;
  ccf.kv[table2].forEach(function(value2, key2, tbl2) {
    const row2 = JSON.parse(ccf.bufToStr(tbl2.get(key2)));
    const join_val2 = row2[index2];
    if (hashmap.has(join_val2)) {
      hashmap.get(join_val2).forEach(function(elt) {
          const merged_row = elt.concat(row2);
          const k = ccf.strToBuf(index.toString()); 
          const v = ccf.strToBuf(JSON.stringify(merged_row));
          ccf.kv["join"].set(k, v);
          // results.push(merged_row);
          index += 1;
      });
    }
  });
  console.log(index); 
  return results;
}

function join(table1, index1, table2, index2) {
  const results = []; 
  ccf.kv[table1].forEach(function(value, key, tbl1) {
    const row = JSON.parse(ccf.bufToStr(tbl1.get(key)));
    const join_val = row[index1];
    ccf.kv[table2].forEach(function(value2, key2, tbl2) {
      const row2 = JSON.parse(ccf.bufToStr(tbl2.get(key2)));
      const join_val2 = row2[index2];
      if (join_val === join_val2) {
        results.push(join_val);
      }
    });
  });
  return results;
}

function distinct(arr) {
  var seen = {};
  var ret_arr = [];
  ccf.kv["select"].forEach(function(value, key, tbl) {
    if (ccf.kv["distinct"].has(value) === false) {
      ccf.kv["distinct"].set(value, value);  
      ret_arr.push(value)
    }
  });
  // for (var i = 0; i < arr.length; i++) {
  // 	if (!(arr[i] in seen)) {
  // 		ret_arr.push(arr[i]);
  // 		seen[arr[i]] = true;
  // 	}
  // }
  return ret_arr;
}

export function run_query(request) {
  const tbl1name = "orders1";
  const tbl2name = "orders2";
  console.log('after');
  let params = request.body.json();
  if ("query" in params === false) {
    throw new Error(`No query provided`);
  }
  console.log(params);
  if (params.query !== "query1") {
    throw new Error(`Invalid query: must be query1 lol`);
  }

  // const join_results = hashjoin(tbl1name, 1, tbl2name, 1);
  const join_results = hashjoin(tbl1name, 1, tbl2name, 1);
  console.log('finished join');
  const select_results = select(join_results, 1);
  console.log('finished select');
  const distinct_results = distinct(select_results);
  console.log('finished distinct');
  const ret = JSON.stringify(distinct_results);
  return { body: { results: ret } };
}
