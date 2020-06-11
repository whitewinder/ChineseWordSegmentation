#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) wangwenhua 971112338.com, Inc. All Rights Reserved
#
########################################################################

import kenlm
model = kenlm.Model('weixin.klm')

from math import log10

#这里的转移概率是人工总结的，总的来说，就是要降低长词的可能性。
trans = {'bb':1, 'bc':0.15, 'cb':1, 'cd':0.01, 'db':1, 'de':0.01, 'eb':1, 'ee':0.001}
trans = {i:log10(j) for i,j in trans.iteritems()}


def viterbi(nodes):
    paths = nodes[0]
    for l in range(1, len(nodes)):
        paths_ = paths
        paths = {}
        for i in nodes[l]:
            nows = {}
            for j in paths_:
                if j[-1]+i in trans:
                    nows[j+i]= paths_[j]+nodes[l][i]+trans[j[-1]+i]
            k = nows.values().index(max(nows.values()))
            paths[nows.keys()[k]] = nows.values()[k]
    return paths.keys()[paths.values().index(max(paths.values()))]


def cp(s):
    return (model.score(' '.join(s), bos=False, eos=False) - model.score(' '.join(s[:-1]), bos=False, eos=False)) or -100.0


def mycut(s):
    nodes = [{'b':cp(s[i]), 'c':cp(s[i-1:i+1]), 'd':cp(s[i-2:i+1]), 'e':cp(s[i-3:i+1])} for i in range(len(s))]
    tags = viterbi(nodes)
    words = [s[0]]
    for i in range(1, len(s)):
        if tags[i] == 'b':
            words.append(s[i])
        else:
            words[-1] += s[i]
    return words


if __name__ == '__main__':
    s = "林心如和易烊千玺一同录制了江苏卫视的一档节目，从此支撑着该公司各项目的顺利进展。"
    mycut()