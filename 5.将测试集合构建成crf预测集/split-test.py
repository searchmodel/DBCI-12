#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os
import sys
import io
import re

from pandas import Series, DataFrame 
import jieba
import jieba.posseg as pseg


path = "C:/word2vec/pyltp";
train_file = "泰一指尚-评测集.csv"
jieba.load_userdict(path+'/model/nopos_word_file.txt')#all-newword.txt

topic_word_crf_test_file = open(path+'/新思路梳理-备份baseline-20170108230000/新思路梳理/5.将测试集合构建成crf预测集/code/topic_word_crf_test.txt', 'w+',encoding='UTF-8')


# 切词，词性标注，文法解析
file = open(path+"/"+train_file,encoding="UTF-8")
data = {}
print("开始构建出数据...")
while 1:
	line = file.readline().strip()	
	if not line:
		break
	id = line[0:line.index(",")]
	ct = line[line.index(",")+1:]
	#data[id] = ctx	
	print(id)
	#print(ct)
	words_pos = pseg.cut(str(ct))# 分词+词性标注
	postags_list = []
	words_list = []
	for word, flag in words_pos:
		postags_list.append(flag)
		words_list.append(word)
		#print('%s %s' % (word, flag))
		if ord != '' and word != ' ' and word != '\t' and word != "　":
			topic_word_crf_test_file.write(str(word)+"\t"+str(flag)+"\n")
	topic_word_crf_test_file.write("\n")


topic_word_crf_test_file.flush()
topic_word_crf_test_file.close()


