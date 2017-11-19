#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os
import sys
import io
import re

from pandas import Series, DataFrame 

path = "C:/word2vec/pyltp";
train_file = "泰一指尚-评测集.csv"


file = open(path+'/'+train_file,encoding="UTF-8")
data = {}
for line in file.readlines():
	line = line.strip()	
	id = line[0:line.index(",")]
	ct = line[line.index(",")+1:]
	data[id]=ct


submit_test_file = open(path+'/新思路梳理-备份baseline-20170108230000/新思路梳理/6.基于crf预测结果/code/验证test.txt',encoding="UTF-8")

submit_file = open(path+'/新思路梳理-备份baseline-20170108230000/新思路梳理/6.基于crf预测结果/code/提交.txt', 'w+',encoding='UTF-8')

for line in submit_test_file.readlines():
	line = line.strip()
	id = line[0:line.index(",")]
	ct = line[line.index(",")+1:]
	submit_file.write(str(id)+","+str(data[id])+","+str(ct)+"\n")
	print(str(id))



submit_file.flush()
submit_file.close()