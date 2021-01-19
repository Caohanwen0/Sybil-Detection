import numpy as np
import pandas as pd
import random


def FindInterval(a, arr):
    for i in range(len(arr)):
        if arr[i] >= a:
            return i


V0 = 500
p = 2
VertexList = [i for i in range(V0)]
ArcList = [[] for i in range(V0)]
# 下面每个点随机产生两条边
for i in range(V0):
    randedge = random.sample(range(V0), 2)
    if randedge[0] not in ArcList[i]:
        ArcList[i].append(randedge[0])
    if randedge[1] not in ArcList[i]:
        ArcList[i].append(randedge[1])
    if i not in ArcList[randedge[0]]:
        ArcList[randedge[0]].append(i)
    if i not in ArcList[randedge[1]]:
        ArcList[randedge[1]].append(i)
E0 = 0
for i in range(V0):
    E0 += len(ArcList[i])
print('E0:'+str(E0))
# 至此，G0已构造完成
# 下面，我们开始往PA中添加新节点，共需添加8790-500=8290个节点，每个节点随机产生1或2或3条边。
New = 8290
curnum = E0
num = [0]
for j in range(New):
    VertexList.append(V0+j)
    ArcList.append([])
    num = random.sample([1, 2, 3], 1)
    dist = []
    tail = 0
    for i in range(V0+j):
        tail += len(ArcList[i])
        dist.append(tail/curnum)
    # print('tail:'+str(tail)+'. curnum:'+str(curnum))
    # print('dist:'+str(dist))
    for i in range(num[0]):
        ran = random.random()
        # print('ran:'+str(ran))
        x = FindInterval(ran, dist)
        if V0+j not in ArcList[x]:
            ArcList[x].append(V0+j)
            curnum += 1
            ArcList[V0+j].append(x)
            curnum += 1
E = 0
for i in range(len(ArcList)):
    E += len(ArcList[i])
print('E:'+str(E))
ArcArr = np.array(ArcList)
for i in range(len(ArcArr)):
    print(len(ArcArr[i]))
print(np.max(ArcArr))
# 至此，PA模型构建sybil region完毕。我们应该读取Facebook social network数据集，然后进行网络合并。不过还是先把刚生成的网络存成txt吧。
fileStr = ''
for i in range(len(ArcArr)):
    for j in range(len(ArcArr[i])):
        fileStr += str(VertexList[i])+' '+str(ArcArr[i][j])+'\n'
File = open('PAnetwork.txt', 'w')
File.write(fileStr)
File.close()

