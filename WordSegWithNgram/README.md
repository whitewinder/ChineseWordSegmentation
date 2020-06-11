# 无监督语言模型分词

## 训练过程

首先来训练语言模型。这里文本数据是50万微信公众号的文章，约2GB大小，训练语言模型用的是传统的“统计+平滑”的方法，使用[kenlm](https://github.com/kpu/kenlm)这个工具来训练。

kenlm是一个C++编写的语言模型工具，具有速度快、占用内存小的特点，也提供了Python接口。首先下载编译它：

```shell
wget -O - http://kheafield.com/code/kenlm.tar.gz |tar xz 
cd kenlm
./bjam -j4
python setup.py install
```

接着处理训练语料。kenlm的输入很灵活，不用预先生成语料文本，而可以通过管道的方式传递。比如先编写一个p.py。这一步其实很简单，就是把你要训练的文本分好词（用空格隔开，如果你是做基于字的模型，就把模型的每个字用空格隔开），然后逐一print出来。

然后就可以训练语言模型了，这里训练一个4-gram的语言模型：

```shell
python p.py|./kenlm/bin/lmplz -o 4 > weixin.arpa
./kenlm/bin/build_binary weixin.arpa weixin.klm
```

arpa是通用的语言模型格式，klm是kenlm定义的二进制格式，klm格式占用空间更少。最后我们就可以在Python中载入了。

```python
import kenlm
model = kenlm.Model('weixin.klm')
model.score('微 信', bos=False, eos=False)
'''
score函数输出的是对数概率，即log10(p('微 信'))，其中字符串可以是gbk，也可以是utf-8
bos=False, eos=False意思是不自动添加句首和句末标记符
'''
```

## 分词实践

```shell
python ngram_cut.py
```



