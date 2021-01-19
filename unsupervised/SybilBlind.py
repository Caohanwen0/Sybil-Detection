import numpy as np
import pandas as pd
import random


def L1(a):
    thesum = 0
    for i in range(len(a)):
        thesum += np.abs(a[i])
    return thesum


def calc(v, arc, ww, pp, qq):
    target_p = [0 for i in range(len(v))]
    for u in range(len(v)):
        temp = qq[u]
        for i in range(len(arc[u])):
            neighbour = arc[u][i]
            temp += 2*pp[neighbour]*ww
        target_p[u] = temp
    target_p = np.array(target_p)
    return target_p


bound = 50000
# 我们只取soc-Epinions.txt中的前五万个节点
file1 = open('soc-Epinions1.txt', 'r')
lineList = file1.readlines()
desire = []
for i in range(len(lineList)):
    line = lineList[i]
    if i < 4:
        continue
    line = line[:-1]
    curlist = line.split('\t')
    for j in range(len(curlist)):
        curlist[j] = int(curlist[j])
    if curlist[0] >= bound or curlist[1] >= bound:
        continue
    desire.append(curlist)
# print(len(desire)) # 共有464627条边在benign region中。
file1.close()
file2 = open('PAnetwork.txt', 'r')
lineList2 = file2.readlines()
desire2 = []
for i in range(len(lineList2)):
    curlist = lineList2[i][:-1]
    curlist = curlist.split(' ')
    for j in range(len(curlist)):
        curlist[j] = int(curlist[j])
    # print(curlist)
    desire2.append(curlist)
file2.close()
# 现在，我们考虑将这两个图合并起来。原网络索引不变，依然为0-49999，PA生成网络索引变为50000-58789
VertexList = [i for i in range(bound+8790)]
ArcList = [[] for i in range(len(VertexList))]
for i in range(len(desire)):
    cur = desire[i]
    if cur[0] not in ArcList[cur[1]]:
        ArcList[cur[1]].append(cur[0])
    if cur[1] not in ArcList[cur[0]]:
        ArcList[cur[0]].append(cur[1])
for i in range(len(desire2)):
    cur = desire2[i]
    cur[0] += bound
    cur[1] += bound
    if cur[0] not in ArcList[cur[1]]:
        ArcList[cur[1]].append(cur[0])
    if cur[1] not in ArcList[cur[0]]:
        ArcList[cur[0]].append(cur[1])
# 现在，我们考虑产生attack edges，就先考虑产生1000条吧。随机从原社交网络中选1000个点，随即从PA网络中选1000个点，然后一一连接即可。
attack_edges = 1000
nodes1 = np.random.choice(VertexList[:bound], attack_edges)
nodes2 = np.random.choice(VertexList[bound:], attack_edges)
for i in range(attack_edges):
    if nodes1[i] not in ArcList[nodes2[i]]:
        ArcList[nodes2[i]].append(nodes1[i])
    if nodes2[i] not in ArcList[nodes1[i]]:
        ArcList[nodes1[i]].append(nodes2[i])
# file3 = open('FormalNetwork.txt', 'w')
# saveStr = ''
# for i in range(len(VertexList)):
#     for j in range(len(ArcList[i])):
#         saveStr += str(i)+' '+str(ArcList[i][j])+'\n'
# file3.write(saveStr)
# 至此，我们完成了网络的构建。下面将0-49999的节点标签置为0（benign users），将50000-58789置为1（sybils）。
labels = []
for i in range(len(VertexList)):
    if i < 50000:
        labels.append(0)
    else:
        labels.append(1)
# 下面，我们设置模型参数。
theta = 0.9
eclipse = 1e-6
w = 1/1000
T = 100
# 下面，我们进行SybilSCAR算法(训练集只选出benign users和sybils各20个)。
N = 20


def SybilSCAR():
    selected = random.sample(VertexList, N)
    benign_selected = selected[:int(N/2)]
    sybil_selected = selected[int(N/2):]
    myStr = ''
    for i in range(len(selected)):
        if i < int(N/2):
            myStr += str(benign_selected[i]) + ' '
        else:
            myStr += str(sybil_selected[i-int(N/2)]) + ' '
    # sybil_selected = random.sample(VertexList[50000:], N)
    q = []
    for i in range(len(VertexList)):
        # if i < 50000:
        #     if i in benign_selected:
        #         q.append(1-theta)
        #     else:
        #         q.append(0.5)
        # else:
        #     if i in sybil_selected:
        #         q.append(theta)
        #     else:
        #         q.append(0.5)
        if i in benign_selected:
            q.append(1-theta)
        elif i in sybil_selected:
            q.append(theta)
        else:
            q.append(0.5)
    q = np.array(q) - 0.5
    p = q
    t = 1
    while t < T:
        t += 1
        next_p = calc(VertexList, ArcList, w, p, q)
        if L1(next_p-p)/L1(next_p) < eclipse:
            break
        p = next_p
        # print('t:'+str(t))
        # print(p[:10])
        # print(p[-10:])
    p = p + 0.5
    # print(p)
    # print('度大于500的节点：')
    # themax = 500
    # for i in range(len(VertexList)):
    #     if len(ArcList[i]) > themax:
    #         print(i)
    # 下面，看我们预测准确度。
    wrong = 0
    for i in range(len(VertexList)):
        if i < 50000:
            if p[i] >= 0.5:
                wrong += 1
        if i >= 50000:
            if p[i] <= 0.5:
                wrong += 1
    accuracy = (len(VertexList)-wrong)/len(VertexList)
    print('正确率为：'+str(accuracy))
    # 下面我们考虑计算homophily h和one-side entropy
    homogeneous_edge = 0
    total = 0
    sybils = 0
    for i in range(len(VertexList)):
        if p[i] > 0.5:
            sybils += 1
        for j in range(len(ArcList[i])):
            if (p[i] > 0.5 and p[j] > 0.5) or (p[i] < 0.5 and p[j] < 0.5):
                homogeneous_edge += 1
                total += 1
            else:
                total += 1
    h = homogeneous_edge/total
    s = sybils/len(VertexList)
    if s > 0.5:
        e = 0
    else:
        e = -s*np.log(s)-(1-s)*np.log(1-s)
    return h, e, accuracy, myStr


# SybilSCAR()
# K = 100
# saveStr = ''
# selected = ''
# for i in range(K):
#     print('第'+str(i)+'次循环。')
#     curh, cure, curacc, mystr = SybilSCAR()
#     saveStr += str(curh) + ' ' + str(cure) + ' ' + str(curacc) + '\n'
#     selected += mystr+'\n'


# file4 = open('result1.txt', 'w')
# file4.write(saveStr)
# file5 = open('selected1.txt', 'w')
# file5.write(selected)
# file4.close()
# file5.close()