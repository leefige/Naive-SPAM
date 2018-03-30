# Experiment 1: Naive Bayes Classifier

## 实验平台

- 语言：Python
- 环境：Python 3.6.2rc1

## 数据集来源
- [2006 TREC Public Spam Corpora](https://plg.uwaterloo.ca/~gvcormac/treccorpus06/)

## 文件结构

- scripts/目录下为实验脚本
    - parseData.py包含处理文件、数据相关方法
    - naiveBayes.py包含朴素贝叶斯分类器的定义，定义了NaiveBayes类
    - classify.py包含分类器相关方法，提供了程序入口
    - defs.py包含一些常量定义
    - test.py包含少量单元测试，予以了保留
    - autoTest.bat为自动测试用脚本，用于收集issue1, 2所需数据
- 如需运行，scripts/目录应该与数据集解压后的目录`trec06c-utf8/`处于同一级

## 运行方法

- 运行的工作目录必须为scripts/目录
- 若是第一次运行，请先运行`python parseData.py`，预处理后的数据会存放在data/目录下
- 随后可以使用`python classify.py [-opt]`进行分类测试，命令行参数如下
    - `-i`，使用ip地址作为特征之一
    - `-t`，使用发件时间作为特征之一
    - `-w weight`，设定训练集比重为weight，weight应该在(0, 1]间，默认为0.8
    - `-s smooth`，设定平滑因子α为smooth，smooth应该在(0, 1]间，默认为1e-9