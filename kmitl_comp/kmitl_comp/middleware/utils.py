#/***** refacter array or dict or str from "str" -> str *******/
from copy import deepcopy

def dataRefacter(data_):
    data = deepcopy(data_)
    del data_
    if isinstance(data,list):
        for v in data:
            v = v[1:-1]
    elif isinstance(data,dict):
        for k,v in data.items():
            data[k] = v[1:-1]
    elif isinstance(data,str):
        data = data[1:-1]
    return data