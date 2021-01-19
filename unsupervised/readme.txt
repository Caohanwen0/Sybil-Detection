unsupervised文件夹为无监督学习文件夹：

SybilBlind.py为无监督学习SybilBlind算法的实现。

SybilSCAR.py是随机游走的标签传播算法的实现。

H&S.py文件是运用同质性和熵筛选出正极化样本的代码。

FormalNetwork.txt是soc-Epinions1网络和优先链接模型（PA）生成的网络。

实验验证：

我们选取soc-Epinions数据集的前五万个用户节点极其之间的连边（约46万条连边），全部标为正常用户；然后，通过优先链接（PA）模型生成一个具有8790个节点及其连边的网络（约35000条连边），全部标为虚假用户；最后添加“attack edges”，attack edges即表示正常用户和虚假用户之间的连边（由于同质网络的假设，要注意不能生成过多attack edges）。我们分别添加100、500、1000、3000、5000、8000、10000、15000、20000、30000、50000、100000条attack edges，将预测结果得到的accuracy、precision以及recall指标绘制成三条随attack edges数量变化的曲线如下：
 
![image](https://github.com/Slam1423/Sybil-Detection/blob/main/unsupervised/Accuracy%2C%20precision%2C%20recall%20with%20different%20attack%20edges1.png)
![image](https://github.com/Slam1423/CIFAR-10-Classification-by-Lenet-5-and-ResNet18/blob/main/lenet5.jpg)
不难发现，当attack edges个数小于10000时，该网络保持有比较好的预测性能，可认为该网络属于同质网络；而当attack edges个数大于10000时，该网络对虚假用户的预测性能变得很差，可认为此时其不再满足同质性假设，从而不再适用于SybilBlind算法。由此，我们也可以了解到当网络中异质边占所有边的比例小于2%时，可认为该网络为同质网络；否则应认为该网络不是同质网络。
