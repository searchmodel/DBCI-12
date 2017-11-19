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
nopos_word_file_path = "C:/word2vec/pyltp/新思路梳理/1.训练集构建词典/nopos_word_file.txt"
z_word_file_path = "C:/word2vec/pyltp/新思路梳理/1.训练集构建词典/正_word_file.txt"
f_word_file_path = "C:/word2vec/pyltp/新思路梳理/1.训练集构建词典/负_word_file.txt"
m_word_file_path = "C:/word2vec/pyltp/新思路梳理/1.训练集构建词典/中_word_file.txt"

df = pd.read_excel(path+"/"+train_file, encoding="UTF-8",skiprows=None)
df = df.fillna("")

nopos_word_file = open(nopos_word_file_path, 'w+',encoding='UTF-8')
z_word_file = open(z_word_file_path, 'w+',encoding='UTF-8')
f_word_file = open(f_word_file_path, 'w+',encoding='UTF-8')
m_word_file = open(m_word_file_path, 'w+',encoding='UTF-8')

set_word = []
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
			
	#print(theme_spts)
	#print(word_spts)
	#print(anls_spts)
	#print(new_anls_spts)
	# 无词性词典
	for ts in theme_spts:
		if ts != 'NULL':
			if ts not in set_word:
				nopos_word_file.write(ts+"\n")
				set_word.append(ts)
	for bindex in range(0,len(word_spts)):
		ts = word_spts[bindex]
		ans = anls_spts[bindex]
		if ts != 'NULL':
			if ts not in set_word:
				nopos_word_file.write(ts+"\n")				
				set_word.append(ts)
				if ans == "1":
					z_word_file.write(ts+"\n")		
				elif ans == "-1":
					f_word_file.write(ts+"\n")	
				else:
					m_word_file.write(ts+"\n")

nopos_word_file.flush();
nopos_word_file.close();

z_word_file.flush();
z_word_file.close();

f_word_file.flush();
f_word_file.close();

m_word_file.flush();
m_word_file.close();


