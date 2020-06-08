#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) wangwenhua 971112338.com, Inc. All Rights Reserved
#
########################################################################

from collections import defaultdict


#  加载词典
def load_dict(path):
    word_dict = set()  # 创建一个去重集合
    with open(path, 'r', encoding='UTF-8') as f:
        for line in f:
            word_dict.add(
                line.strip())
    return word_dict


# 正向最大匹配算法
# 原则：颗粒度越大越好
# 返回list[tuple(word, len)]的形式, tuple[0]为词,tuple[1]为词的长度，当长度为0时代表该词为非词典词
def MaxMatch(sentence, max_len, word_dict):  # max_len是最大词长度
    # current_word_start_index记录当前词的词首index
    # next_word_start_index记录下一个词的词首index
    # j是以当前词的词首current_word_srart_index为起点，顺序往前寻找下一个词词首的index
    if not sentence or sentence is None:
        raise Exception("sentence can not be empty or None")  # 句子不能为空  #如果引发Exception异常，后面的代码将不能执行
    result = []
    current_word_start_index = 0
    while current_word_start_index < len(sentence):
        end = current_word_start_index + max_len if current_word_start_index + max_len < len(sentence) else len(sentence)
        temp = sentence[current_word_start_index]
        next_word_start_index = current_word_start_index
        for j in range(current_word_start_index + 1, end + 1):
            if sentence[current_word_start_index:j] in word_dict:  # 词典分割
                temp = sentence[current_word_start_index:j]
                next_word_start_index = j
        if next_word_start_index == current_word_start_index:  # 单字且非词典词(一个都没匹配到)
            result.append((temp, 0))
            current_word_start_index += 1
        else:
            result.append((temp, len(temp)))
            current_word_start_index = next_word_start_index
    return result


# 逆向匹配算法
# 原则：颗粒度越大越好
# 返回list[tuple(word, len)]的形式, tuple[0]为词,tuple[1]为词的长度，当长度为0时代表该词为非词典词
def ReverseMaxMatch(sentence, max_len, word_dict):
    # current_word_end_index记录当前词的词尾index
    # next_word_end_index记录下一个词的词尾index
    # j是以当前词的词尾current_word_end_index为起点，倒叙往前寻找下一个词词尾的index
    if not sentence or sentence is None:
        raise Exception("sentence can not be empty or None")
    result = []
    current_word_end_index = len(sentence) - 1
    while current_word_end_index >= 0:
        start = current_word_end_index - max_len + 1 if current_word_end_index - max_len + 1 > 0 else 0
        temp = sentence[current_word_end_index]
        next_word_end_index = current_word_end_index
        for j in range(start, current_word_end_index + 1):
            if sentence[j:current_word_end_index + 1] in word_dict:
                temp = sentence[j:current_word_end_index + 1]
                next_word_end_index = j - 1
                break  # 因为j是从小变大的，[j:i+1]是的长度是从大变小的，根据最大匹配算法，优先匹配到的一定是最长的，所以break
        if next_word_end_index == current_word_end_index:  # 单字且非词典词(一个都没匹配到)
            result.append((temp, 0))
            current_word_end_index -= 1
        else:
            result.append((temp, len(temp)))
            current_word_end_index = next_word_end_index
    result.reverse()  # 因为是逆向匹配的，所以是倒叙，需要reverse一下
    return result


# 双向最大匹配
# 切分结果中非词典词越少越好，单字字典词数越少越好
def BothwayMaxMatch(sentence, max_len, word_dict):
    if not sentence or sentence is None:
        raise Exception("sentence can not be empty or None")
    foward_result = MaxMatch(sentence, max_len, word_dict)
    backward_result = ReverseMaxMatch(sentence, max_len, word_dict)

    def count_result(result):  # 词计数(多字词的字数-oov字数-单字词字数)，这是基于规则设定，多字词越多越好，oov和单字词越少越好(oov都是单字)
        counter = defaultdict(int)
        for r in result:
            if r[1] == 0:
                counter['OOV'] += 1  # 非词典单词
            # print(counter)
            elif r[1] == 1:
                counter['single'] += 1  # 单字词
                # print(counter)
            else:
                counter['multi'] += r[1]  # 多字词的字数
            # print(counter)
        return counter['multi'] - counter['OOV'] - counter['single']

    foward_count = count_result(foward_result)
    backward_count = count_result(backward_result)
    if foward_count > backward_count:
        return foward_result
    else:
        return backward_result


path = 'word_dict.txt'
max_len = 3  # max_len是最大词长度，如'动物'、'动物园'符合要求，'野生动物园'不符合要求
word_dict = load_dict(path)
result = MaxMatch('我们在野生动物园玩。', max_len, word_dict)
print(result)
result = ReverseMaxMatch('我们在野生动物园玩。', max_len, word_dict)
print(result)
result = BothwayMaxMatch('我们在野生动物园玩。', max_len, word_dict)
print(result)
