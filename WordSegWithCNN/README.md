---
typora-copy-images-to: upload
---

# WordSegWithCNN
卷积神经网络实现中文分词

## 环境依赖
Python2.7
Tensorflow 1.0

最好使用GPU来加速训练过程。

## 数据集
从[这里](https://drive.google.com/open?id=0B-f0oKMQIe6sQVNxeE9JeUJfQ0k)下载数据集'data.zip',解压到目录data。
project结构如下：

   convseg
   |  data
   |  |  datasets
   |  |  |  sighan2005-pku
   |  |  |  |  train.txt
   |  |  |  |  dev.txt
   |  |  |  |  test.txt
   |  |  |  sighan2005-msr
   |  |  |  |  train.txt
   |  |  |  |  dev.txt
   |  |  |  |  test.txt
   |  |  embeddings
   |  |  |  news_tensite.w2v200
   |  |  |  news_tensite.pku.words.w2v50
   |  |  |  news_tensite.msr.words.w2v50
   |  tagger.py
   |  train_cws.py
   |  train_cws.sh
   |  train_cws_wemb.sh
   |  score.perl
   |  README.md

## 模型训练
首先，给bash脚本赋予执行权限:

   chmod +x train_cws.sh train_cws_wemb.sh

训练 Baseline model CONV-SEG（无word embeddings）:

   ./train_cws.sh WHICH_DATASET WHICH_GPU

训练带word embeddings的model WE-CONV-SEG:

   ./train_cws_wemb.sh WHICH_DATASET WHICH_GPU

其中，参数WHICH_DATASET和WHICH_GPU的说明:

WHICH_DATASET可选`pku` and `msr`

WHICH_GPU，如果用CPU训练，词参数为空即可，如果是在gpu0上训练，则设为0。

因此，在gpu0上训练用pku数据集训练CONV-SEG，完整命令为

   ./train_cws.sh pku 0

更多参数设定，请修改`train.py`。

## 测试集score
| Model       | PKU(dev) | PKU(test) | MSR(dev) | MSR(test) |
| :---------- | :------- | :-------- | :------- | :-------- |
| CONV-SEG    | 96.8     | 95.7      | 97.2     | 97.3      |
| WE-CONV-SEG | 97.5     | 96.5      | 98.1     | 98.0      |

## 搭建并启动中文分词服务
服务启动文件，server.py，设置参数task(cws)、model_dir(训练好的模型文件目录)、port(服务端口)

   python server.py --task cws --model_dir xxx --port 8765

![](/Users/wangwenhua/Desktop/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202020-06-09%20%E4%B8%8A%E5%8D%8811.07.55.png)

