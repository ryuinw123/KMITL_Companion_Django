#/***** refacter array or dict or str from "str" -> str *******/
from copy import deepcopy
import jwt

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

def returnUserIdFromToken(token) -> int:
    return int(jwt.decode(token, 'secret', algorithms=['HS256'])['id'])


def returnTypeCodeToName(listOfTypeCode):
    typeCode = {
        0 : "ร้านอาหาร",
        1 : "อาคารเรียน",
        2 : "ห้องเรียน",
        3 : "ร้านค้า",
        4 : "สถานที่",
        5 : "หอพัก",
        6 : "ห้องน้ำ",
        7 : "ธนาคาร",
        99 : "ทั่วไป",
        100 : 100, #bookmark
        969 : 969, #event
    }
    newList = []

    for _listOfTypeCode in listOfTypeCode:
        newList.append(typeCode[_listOfTypeCode])

    if (newList == []):
        newList = [val for val in typeCode.values()]

    return newList

def returnNameToTypeCode(name):
    typeCode = {
        0 : "ร้านอาหาร",
        1 : "อาคารเรียน",
        2 : "ห้องเรียน",
        3 : "ร้านค้า",
        4 : "สถานที่",
        5 : "หอพัก",
        6 : "ห้องน้ำ",
        7 : "ธนาคาร",
        99 : "ทั่วไป",
        100 : 100, #bookmark
        969 : 969, #event
    }

    return [key for key, val in typeCode.items() if val == name][0]