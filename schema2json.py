# -*- coding: utf-8 -*-
'''
Project smoketestbak
Author  zhenghongguang
Date    2019-12-26
'''
import json
import random
import exrex
import rstr
import math

import unittest

def typeString(obj):
    '''
    maxLength default = 20
    minLength default = 5
    如果 pattern不存在，则随机生成任意字母+数字
    :param obj:
    :return:
    '''
    if obj.get("enum"):
        return obj.get("enum")[random.randint(0,len(obj.get("enum"))-1)]
    maxLength = obj.get("maxLength") if obj.get("maxLength") else 20
    minLength = obj.get("minLength") if obj.get("minLength") else 5
    pattern = obj.get("pattern")
    if pattern == None:
        pattern = "[0-9a-zA-Z]{%d,%d}"%(minLength,maxLength)
    #print(pattern)
    return exrex.getone(pattern)

def typeInteger(obj):
    '''
    multipleOf default = 1
    minimum  default = multiple * -5
    maximum  default = maximum * 20
    如果 -multiple < minimum & maximum < multiple rasie error
    :param obj:
    :return:
    '''
    if obj.get("enum"):
        return obj.get("enum")[random.randint(0,len(obj.get("enum"))-1)]
    multiPle = obj.get("multipleOf") if obj.get("multipleOf") else 1
    miniMum = obj.get("minimum") if obj.get("minimum") else -5*multiPle
    maxiMum = obj.get("maximum") if obj.get("maximum") else 20*multiPle
    miniMum = miniMum if obj.get("exclusiveMinimum") else miniMum + 1
    maxiMum = maxiMum if obj.get("exclusiveMaximum") else maxiMum - 1

    if math.ceil(miniMum/multiPle)== 0 and math.ceil(maxiMum/multiPle) == 0:
        raise "get Integer failed,please check"
    return random.randrange(math.ceil(miniMum/multiPle),math.ceil(maxiMum/multiPle)) * multiPle

def typeNumber(obj):
    '''
    随机生成小数，方法与生成整数类似
    如果范围小于 0.0001 会失败
    :param obj:
    :return:
    '''
    if obj.get("enum"):
        return obj.get("enum")[random.randint(0,len(obj.get("enum"))-1)]
    miniNum = obj.get("minimum") if obj.get("minimum") else -5
    maxiNum = obj.get("maximum") if obj.get("maximum") else 20
    miniNum = miniNum if obj.get("exclusiveMinimum") else miniNum + 0.0001
    maxiNum = maxiNum if obj.get("exclusiveMaximum") else maxiNum - 0.0001
    return( random.uniform(miniNum,maxiNum) )

def typeBoolean():
    '''
    :return:
    '''
    return  True if random.randint(0,1) else False

def typeArray(obj):

    '''

    :return:
    '''
    minItem = obj.get("minItems") if obj.get("minItems") else 1
    maxItem = obj.get("maxItems") if obj.get("maxItems") else 10
    arrayData = []
    for i in range(random.randint(minItem,maxItem)):
        if isinstance(obj.get("items"),list):
            ArrayItem = obj.get("items")[random.randint(0,len(obj.get("items"))-1 )]
        else:
            ArrayItem = obj.get("items")
        arrayData.append(obj2Data(ArrayItem))

    return arrayData

def obj2Data(obj):
    if isinstance(obj.get("type"),list):
        typeStr = obj.get("type")[random.randint(0,len(obj.get("type"))-1)]
    else:
        typeStr = obj.get("type")
    if typeStr == "string":
        return  typeString(obj)
    if typeStr == "boolean":
        return  typeBoolean()
    if typeStr == "number":
        return  typeNumber(obj)
    if typeStr == "integer":
        return typeInteger(obj)
    if typeStr == "array":
        return typeArray(obj)
    if typeStr == "object":
        return schema2json(obj)

def schema2json(obj):
    '''

    :param obj:
    :return:
    '''
    objData = {}
    required = obj.get("required") if obj.get("required") else []
    for key in obj.get("properties").keys():
        if key in required:
            objData[key] = obj2Data(obj.get("properties").get(key))
        elif random.randint(0,1):
            objData[key] = obj2Data(obj.get("properties").get(key))
    return objData


class testSchema2json(unittest.TestCase):
    def test_typeString(self):
        print('-------' * 20)
        testObj = [{"enum":["a","b","c"]},
                   {"enum":["a"]},
                   {"enum":[]},
                   {},
                   {"minLength":3,"maxLength":6},
                   {"pattern":"[a-z0-9]{6,8}"}]
        for obj in testObj:
            print(typeString(obj))
        print('-------' * 20)

    def test_typeInteger(self):
        print('-------'*20)
        testObj = [{},
                   {"multipleOf":5},
                   {"multipleOf":5,"minimum":-10,"maximum":10}]
        for obj in testObj:
            print(typeInteger(obj))
        print('-------' * 20)

    def test_typeNumber(self):
        print('-------' * 20)
        testObj = [{},
                   { "minimum": -10, "maximum": 10},
                   { "minimum": -0.000010, "maximum": 0.000010}]
        for obj in testObj:
            print(typeNumber(obj))
        print('-------' * 20)

    def test_typeBoolean(self):
        print('-------' * 20)
        for i in range(5):
            print(typeBoolean())
        print('-------' * 20)

if __name__ == '__main__':
    #print(typeString({"enum":[]}))
    #print(typeInteger({}))
    #unittest.main()
    fr = open("/Users/zhenghongguang/code/smoketestbak/tm_case/schema/job/queryjob/queryjob.json")
    tmpschema = json.load(fr)
    fr.close()
    print(type(tmpschema))
    print(schema2json(tmpschema))

