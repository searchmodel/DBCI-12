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

'''
 没有处理：
	幸福	r	P
	这个	r	S
	中奖	nz	S
	这个	r	T
	中奖	nz	T
	有用吗	v	S

很	zg	P
不错	a	S
要	v	P
比	p	P
婴儿	n	P
店里	n	P
便宜	a	S
好多	m	P
一直	d	P
信赖	n	S
京东自营	x	T
'''

path = "C:/word2vec/pyltp";
train_file = "泰一指尚-评测集.csv"
jieba.load_userdict(path+'/model/nopos_word_file.txt')

file = open(path+'/新思路梳理/4.测试crf模型正确率/crf_valid.csv',encoding="UTF-8")
topic_word_crf_train_valid_file = open(path+'/新思路梳理/4.测试crf模型正确率/code/验证train.txt', 'w+',encoding='UTF-8')

print("开始构建出数据...")

datas = {}
index = 1
item = []
for line in file.readlines():
	line = line.strip()
	#print(line)
	if not line and line == "":
		datas[index] = item
		if index % 100000 == 0:
			print(str(line))
			print(str(index))
		index = index + 1
		item = []
		#break
		continue
	lines = line.split("\t")
	word = lines[0]
	pos = lines[1]
	tag = lines[2]
	#print(word+"\t"+pos+"\t"+tag)
	item.append((word,pos,tag))

# 最小力度的拆解
def getMinTS(items):
	print(items)
	TISEXEC = False	
	iT = []
	iS = []
	iT_count = 0
	iS_count = 0
	for it in items:
		wd = it[0]
		pos = it[1]
		ans = it[2]
		if ans == "T":
			if TISEXEC == True:
				iT.append(wd)
				iS.append("NULL")
				iS.append("NULL")
			else:
				iT.append(wd)
			iT_count = iT_count+1
			TISEXEC=True
		elif ans == "S":
			# T不能为空
			iS_count = iS_count+1
			if TISEXEC == False:
				print("===>"+wd)
				iT.append("NULL")
				iS.append(wd)
				TISEXEC=False
				iT_count = iT_count+1
				#print(T+":"+S)
			else:
				#print("NULL"+":"+S)
				iS.append(wd)
				TISEXEC=False
	#print(str(iT_count))
	#print(str(iS_count))
	if iT_count == 1 and iS_count == 1:#忽略顺序
		if "NULL" in iT and len(iT) != len(iS):
			iT.remove("NULL")
		return (iT,iS)
	if iT_count == 0 and iS_count == 0:
		return (["NULL"],["NULL"])
	print("*********************>")
	if iT_count >= iS_count:
		bu_count = iT_count-iS_count
		print("减法："+str(bu_count))
		for _index in range(0,bu_count):
			iS.append("NULL")
		return (iT,iS)
	if iT_count < iS_count:
		bu_count = iS_count-iT_count
		print("加法："+str(bu_count))
		print("加法："+str(iT))
		print("加法："+str(iS))
		for _index in range(0,bu_count):
			iT.append("NULL")
		return (iT,iS)
	print("T++++++++++++++++>"+str(iT))
	print("S++++++++++++++++>"+str(iS))
	

# 2.句子拆分进行TS抽取，解析复杂情况
def split_sent(items):
	item_sends = {}	
	item_send = []
	item_index = 0
	for ids in range(0,len(items)):
		it = items[ids]
		wd = it[0]
		pos = it[1]
		ans = it[2]
		if len(items)-1 == ids:
			item_send.append((wd,pos,ans))
		if (pos == "x" and (wd == "," or wd == '，' or wd == '。'
				or wd == '.'
				or wd == '？'
				or wd == '?'
				or wd == '！'
				or wd == '!'
				or wd == '['
				or wd == '【'
				or wd == '】'
				or wd == ']'
				) or  len(items)-1 == ids):
			item_sends[item_index] = item_send
			item_index = item_index + 1
			item_send = []
			continue
		item_send.append((wd,pos,ans))
	print(item_sends)
	# 按照顺序进行排列组合输出：，无关顺序
	# T
	# S
	# T,S
	# S,T
	# T,S;T,S
	# S,T;S,T
	# T,T
	# S,S
	iT = []
	iS = []
	for index in item_sends:
		item = item_sends[index]
		rs = getMinTS(item)# x;,y; x;x;,y;y;
		for _it in rs[0]:
			iT.append(_it)
		for _it in rs[1]:
			iS.append(_it)
	
	print(">>>>>>>>>>>>>>>>>>>>>>>>"+str((iT,iS)))
	iT_tmp = []
	iS_tmp = []
	quchong_tmp = []
	for _i in range(0,len(iT)):
		_tt = iT[_i]
		_ss = iS[_i]		
		if _tt == "NULL" and _ss == "NULL":
			continue
		elif _ss == "NULL":
			continue
		elif (str(_tt)+str(_ss)) in quchong_tmp:
			continue
		else:
			quchong_tmp.append(str(_tt)+str(_ss))
			iT_tmp.append(_tt)
			iS_tmp.append(_ss)
	result = "";
	for _i in range(0,len(iT_tmp)):
		_tt = iT_tmp[_i]
		result = result + _tt+";"
	result = result + ","
	for _i in range(0,len(iS_tmp)):
		_ss = iS_tmp[_i]
		result = result + _ss+";"
	return result

# 1. 初步解析=过滤简单无标签，标签都为1的情况
def getT1S1(items):
	T = 0
	S = 0
	TStr = ""
	SStr = ""
	for it in items:
		wd = it[0]		
		pos = it[1]
		ans = it[2]
		if ans == "T":
			TStr = wd
			T = T+1
		if ans == "S":
			SStr = wd
			S = S+1
	print(str(TStr)+";"+str(SStr))
	if T == 0 and S == 0:
		return "NULL;,NULL;"
	elif T == 1 and S == 1:
		if SStr != "NULL" and SStr != "":
			return TStr+";,"+SStr+";"
	else:
		print("拆分情况：")
		#其他情况进行句子拆分
		return split_sent(items)

print("开始计算...")
for dta in datas:
	items = datas[dta]
	outputTag = getT1S1(items)
	topic_word_crf_train_valid_file.write(str(dta)+","+outputTag+"\n")

topic_word_crf_train_valid_file.flush()
topic_word_crf_train_valid_file.close()

