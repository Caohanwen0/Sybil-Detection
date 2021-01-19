import numpy as np
import pandas as pd

file = open('result1.txt', 'r')
lineList = file.readlines()
target = []
for i in range(len(lineList)):
    line = lineList[i].split(' ')
    for j in range(len(line)):
        line[j] = float(line[j])
    target.append(line)
# 下面先按照target的第一个元素对其进行从小到大排序
target.sort(key=lambda x:x[0], reverse=True)
print(target)
k = 10
sublist = target[:k]
sublist.sort(key=lambda x:x[1], reverse=True)
print(sublist)