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
jieba.load_userdict(path+'/model/nopos_word_file.txt')

file = open(path+'/新思路梳理/4.测试crf模型正确率/crf_valid2.csv',encoding="UTF-8")
topic_word_crf_train_valid_file = open(path+'/新思路梳理/4.测试crf模型正确率/code/验证train.txt', 'w+',encoding='UTF-8')

print("开始构建出数据...")

data = []
index = 1

T = []
S = []
TISEXEC=False
T_count = 0
S_count = 0
while 1:
	line = file.readline().strip()	
	if not line and line == "":
		print("---------------------->"+str(index)+"---"+str(T)+"---"+str(S))
		print(index)
		while len(T) != len(S):
			# 如果只有一个S一个T，不关注顺序
			print("T_count："+str(T_count)+", S_count:"+str(T_count))
			if T_count == 1 and S_count == 1:
				print("一个S一个T")
				T.remove("NULL")
			elif T_count == 0 and S_count == 0:
				print("无S无T")
			elif len(T) > len(S):
				S.append("NULL")
		txt = ""
		for ttt in T:
			txt = txt+ttt+";"
		sxs = ""
		for sss in S:
			sxs = sxs+sss+";"
		topic_word_crf_train_valid_file.write(str(index)+","+txt+","+sxs+"\n")
		
		index = index+1
		T = []
		S = []
		T_count = 0
		S_count = 0
		break
		#continue
	lines = line.split("\t")
	word = lines[0]
	pos = lines[1]
	tag = lines[2]
	print(word+"\t"+pos+"\t"+tag)
	
	if pos == "x":# 标点符号
				
	if tag == "T":
		T.append(word)
		T_count = T_count+1
		TISEXEC=True
	elif tag == "S":
		# T不能为空
		S_count = S_count+1
		if TISEXEC == False:
			print("===>"+word)
			T.append("NULL")
			S.append(word)
			TISEXEC=False
			#print(T+":"+S)
		else:
			#print("NULL"+":"+S)
			S.append(word)
			TISEXEC=False

		
	
	

topic_word_crf_train_valid_file.flush()
topic_word_crf_train_valid_file.close()
	
	
	
	