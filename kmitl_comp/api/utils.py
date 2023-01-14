#/***** refacter array or dict or str from "str" -> str *******/
from copy import deepcopy

def dataRefacter(data_):
    data = deepcopy(data_)
    del data_
    if isinstance(data,list):
        for v in data:
            v = v.strip('"')
    elif isinstance(data,dict):
        for k,v in data.items():
            data[k] = v.strip('"')
    elif isinstance(data,str):
        data = data.strip('"')
    return data