#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os
import sys
import io
import re

import jieba
import jieba.posseg as pseg



path = "C:/word2vec/pyltp";
train_file = "泰一指尚训练集.xlsx"
jieba.load_userdict(path+'/model/nopos_word_file.txt')#all-newword.txt
print("加载词典完毕...")
df = pd.read_excel(path+"/"+train_file, encoding="UTF-8",skiprows=None)
df = df.fillna("")

topic_word_train_file = open(path+'/新思路梳理-备份baseline-20170108230000/新思路梳理/2.通过词典分词构建crf输入集合/code/topic_word_crf_train.txt', 'w+',encoding='UTF-8')
topic_word_valid_file = open(path+'/新思路梳理-备份baseline-20170108230000/新思路梳理/2.通过词典分词构建crf输入集合/code/topic_word_valid.txt', 'w+',encoding='UTF-8')

for index in df.index:
	id = df.iloc[index]["row_id"]
	ct = df.iloc[index]["content-评论内容"]
	theme = df.iloc[index]["theme-主题"]
	word = df.iloc[index]["sentiment_word-情感关键词"]
	anls = df.iloc[index]["sentiment_anls-情感正负面"]	
	print(id)
	#print(ct)
	theme_spts = [item for item in filter(lambda x:x != '', re.split(';',theme))]
	word_spts = [item for item in filter(lambda x:x != '', re.split(';',word))]
	anls_spts = [item for item in filter(lambda x:x != '', re.split(';',anls))]	
	new_anls_spts = []
	for bindex in range(0,len(theme_spts)):
		if bindex < len(anls_spts):
			new_anls_spts.append(str(anls_spts[bindex]))
		else:
			new_anls_spts.append("0")
	#print(""+str(theme_spts))	
	#print(""+str(word_spts))	
	#rint(""+str(anls_spts))	
	words_pos = pseg.cut(str(ct))
	postags_list = []
	words_list = []
	for word, flag in words_pos:
		postags_list.append(flag)
		words_list.append(word)
		tag = "P"
		for ts in theme_spts:
			if ts in word:
				tag = "T"
				break
		for ts in word_spts:
			if ts in word:
				tag = "S"
				break
		if word != '' and word != ' ' and word != '\t' and word != "　":
			#print('%s %s %s' % (word, flag, tag))
			topic_word_train_file.write(str(word)+"\t"+str(flag)+"\t"+str(tag)+"\n")
			topic_word_valid_file.write(str(word)+"\t"+str(flag)+"\n")
	topic_word_train_file.write("\n")
	topic_word_valid_file.write("\n")

topic_word_train_file.flush()
topic_word_train_file.close()

topic_word_valid_file.flush()
topic_word_valid_file.close()

