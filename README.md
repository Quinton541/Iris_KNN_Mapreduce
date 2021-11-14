# FBDP 作业7 

## 191840265 吴偲羿

### 0.文件夹目录

![image-20211114173002784](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114173002784.png)

Data储存输入文件 为已经分好测试集训练集的iris数据集子集

Python_Code内：

![image-20211114173346183](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114173346183.png)

dataDivide为通过sklearn中train_test_split库函数划分训练集测试集代码

Iris_Curves为绘制Iris数据集相关图表的函数

Result储存输出结果

src为java源码

### 2.设计思路

mapreduce实现KNN算法现成思路挺多的 我参考了https://blog.csdn.net/qq_39009237/article/details/86346762的算法实现

总体思路为：

在map中完成测试集合本地训练集的距离计算，reduce端完成排序和挑选。但是由于数据是巨量的，在reduce中完成排序是不实际的。通过自定义数据类型Rose(Iris鸢尾花 Rose玫瑰 挺好)，利用shuffle过程完成自动的排序。实验本质上是一个top N问题，在选择top N的算法上可以压缩到O(N)的算法复杂度，要充分利用map端的combiner来减少mapreduce的网络通信量。具体做法是对于每一个测试数据在本地只发送前k个数据，即将本地距离最近的k个发送出去。
map中完成距离的计算和发送特定的键值对，使其自动排序

combiner是在排好序后，在本地进行对每个id值发送k条数据的限制。有效地较少数据量。

Reduce完成的是将从各个map中接受到的数据和combiner类似，对每个测试数据id只处理前k个，因为使用了自定义数据类型，数据会按照距离排好序，相同id会聚集在一起。所以在处理时会非常方便。因为此时处理的顺序是按原数据行处理的，同时使用了Verify文件进行验证，最终计算出正确率


### 3.划分数据

我们采用了python sklearn库中train_test_split函数 对iris数据集进行划分 为了处理数据方便 我们将鸢尾花的label抽象为 1.2.3 如下：

![image-20211114175452115](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114175452115.png)

第五列即为label。

由于训练集与测试集划分的随机性，我们重复执行dataDivide.py 5次，得到五组数据，并划分成train.csv,test.csv与verify.csv 供程序读取：

![image-20211114175854680](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114175854680.png)

### 4.程序执行及结果

对于每一组数据以及固定的k值 我们执行一次程序 获取结果 运行截图及结果如下（以k=5为例）（正好night_shift mac的ui变成了深色模式）

![image-20211114180159906](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114180159906.png)

![image-20211114180320965](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114180320965.png)

结果如下：

~~~
Sepal.Length,Sepal.Width,Petal.Length,Petal.Width,Predicted Value,True Value
6.9,3.1,5.1,2.3,3,3
6.6,3,4.4,1.4,2,2
5.6,3,4.1,1.3,2,2
6.1,2.6,5.6,1.4,3,3
6.4,3.1,5.5,1.8,3,3
6.9,3.1,4.9,1.5,2,2
7.2,3.6,6.1,2.5,3,3
6.5,2.8,4.6,1.5,2,2
6.4,2.7,5.3,1.9,3,3
5.8,2.7,5.1,1.9,3,3
5.3,3.7,1.5,0.2,1,1
6,2.7,5.1,1.6,3,2
6.3,2.8,5.1,1.5,3,3
7.7,3,6.1,2.3,3,3
7.7,2.8,6.7,2,3,3
5.7,3,4.2,1.2,2,2
6,2.2,4,1,2,2
6.7,3.3,5.7,2.5,3,3
4.8,3.1,1.6,0.2,1,1
5.4,3,4.5,1.5,2,2
5,3.4,1.6,0.4,1,1
4.9,3.1,1.5,0.1,1,1
5.5,2.5,4,1.3,2,2
5.4,3.7,1.5,0.2,1,1
5,3.3,1.4,0.2,1,1
6.2,2.2,4.5,1.5,2,2
6.4,2.8,5.6,2.2,3,3
7.4,2.8,6.1,1.9,3,3
5.4,3.4,1.5,0.4,1,1
5.5,3.5,1.3,0.2,1,1
6.7,2.5,5.8,1.8,3,3
5.2,3.4,1.4,0.2,1,1
4.6,3.6,1,0.2,1,1
4.6,3.1,1.5,0.2,1,1
7.3,2.9,6.3,1.8,3,3
6.7,3.3,5.7,2.1,3,3
6.7,3,5,1.7,3,2
6.5,3,5.2,2,3,3
5.7,4.4,1.5,0.4,1,1
4.8,3,1.4,0.1,1,1
5.7,2.5,5,2,3,3
4.7,3.2,1.6,0.2,1,1
5.1,3.7,1.5,0.4,1,1
4.4,3.2,1.3,0.2,1,1
5.1,3.8,1.6,0.2,1,1
Distance calculation method:osjl
k:5
accuracy:93.33333333333333%

~~~

同时，在程序中更改默认k值为3，10，对5组数据分别执行程序，获得输出至不同文件，此时hdfs文件系统内容如下：

![image-20211114180535152](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114180535152.png)

获得不同k值下精确度，做表作图如下：

|      | k=3   | k=5   | k=10  |
| ---- | ----- | ----- | ----- |
| 1    | 95.56 | 93.33 | 93.33 |
| 2    | 95.56 | 97.78 | 97.78 |
| 3    | 93.33 | 93.33 | 95.56 |
| 4    | 97.78 | 97.78 | 97.78 |
| 5    | 95.56 | 95.56 | 97.78 |

![image-20211114180632701](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114180632701.png)

我们可以看出，也许数据集较小，预测准确率随k值变化并不明显，查阅相关资料得知：在 KNN算法中，k的取值⼀一般不不超过训练样本数的平⽅方根。实际应⽤用中，可以采⽤用 交叉验证法 来选择最优的 k 值。

### 5.有关Iris鸢尾花数据集的一些作图与结论

我们查看预测结果 发现预测失误的点集中在Setosa与Versicolor两类，因此猜想两类鸢尾花数据应当类似。

然而 由于有四个变量，传统的二维平面图与三维立体图均无法直观反应数据集的相似性，我们采用Andrews Curves 将每个样本的多变量量属性值转化为傅⾥里里叶级数的系数来创建曲线：

![image-20211114181321662](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114181321662.png)

相应的 我们还有Parallel coordinates与radviz图对多属性的数据进行维度压缩的可视化处理，作图如下：

![B15A79F63ACA760D034BBCFFEF9054B0](/Users/quinton_541/Library/Containers/com.tencent.qq/Data/Library/Caches/Images/B15A79F63ACA760D034BBCFFEF9054B0.png)

![6117613FDF8BB744599C853618ABF596](/Users/quinton_541/Library/Containers/com.tencent.qq/Data/Library/Caches/Images/6117613FDF8BB744599C853618ABF596.png)

![0A317635BD5B1C3C7AAF20217D9987BD](/Users/quinton_541/Library/Containers/com.tencent.qq/Data/Library/Caches/Images/0A317635BD5B1C3C7AAF20217D9987BD.png)

这样，setosa和versicolor的相似性就十分直观了，这也造成了测试集在预测上的一些malfunction。

### 6.遇到的问题

总体上还是非常顺利的 除了一个折磨人的 IDE抽风问题

原因至今未知，如下：

![6E81C6BE7CF52EF7AB255167368120F3](/Users/quinton_541/Library/Containers/com.tencent.qq/Data/Library/Caches/Images/6E81C6BE7CF52EF7AB255167368120F3.jpg)

![image-20211114181908046](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114181908046.png)

![image-20211114181920252](/Users/quinton_541/Library/Application Support/typora-user-images/image-20211114181920252.png)

约莫就是 全世界人民都没有出现的问题 在541的电脑上出现了，无法解析addCacheFile与getCacheFile两个关键字 也大概就是尝试了一个多小时各种歪门邪道还是没法解决

一气之下 重装IDEA 问题就 莫名其妙解决了

于是541 有感而发：

重装ide解决一切魑魅魍魉 重装ide解决不了的就重装系统 重装系统解决不了的就重买电脑 重买电脑解决不了的建议重开。

完。