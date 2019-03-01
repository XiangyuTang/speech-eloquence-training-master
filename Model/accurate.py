# !/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "zpgao"

import sys
import pinyin
import jieba
import string
import re

FILE_PATH = "./dict/token_freq_pos%40350k_jieba.txt"
PUNCTUATION_LIST = string.punctuation
PUNCTUATION_LIST += "。，？：；｛｝［］‘“”《》／！％……（）"

# 构建词典 一个词对一个数字
def construct_dict( file_path ):
	
	word_freq = {}
	f = open(file_path, 'r', encoding = 'UTF-8')
	for line in f:
		info = line.split(' ')
		word = info[0]
		frequency = info[1]
		word_freq[word] = frequency
	# print('word_freq is : ', word_freq)
	return word_freq

#
def load_cn_words_dict( file_path ):
	cn_words_dict = ""
	f = open(file_path, 'r', encoding = 'UTF-8')
	for word in f:
#		cn_words_dict += word.strip().decode("utf-8")
		cn_words_dict += word.strip()
	# print('cn_words_dict is : ',cn_words_dict)
	return cn_words_dict


def edits1(phrase, cn_words_dict):
	"All edits that are one edit away from `phrase`."
#	phrase = phrase.decode("utf-8")
	phrase = phrase
	splits     = [(phrase[:i], phrase[i:])  for i in range(len(phrase) + 1)]
	deletes    = [L + R[1:]                 for L, R in splits if R]
	transposes = [L + R[1] + R[0] + R[2:]   for L, R in splits if len(R)>1]
	replaces   = [L + c + R[1:]             for L, R in splits if R for c in cn_words_dict]
	inserts    = [L + c + R                 for L, R in splits for c in cn_words_dict]
	return set(deletes + transposes + replaces + inserts)

def known(phrases): return set(phrase for phrase in phrases if phrase.encode("utf-8") in phrase_freq)


def get_candidates( error_phrase ):
	
	candidates_1st_order = []
	candidates_2nd_order = []
	candidates_3nd_order = []

	# error_pinyin = pinyin.get(error_phrase, format="strip", delimiter="/").encode("utf-8")
	error_pinyin = pinyin.get(error_phrase, format="strip", delimiter="/")

	for candidate_phrase in candidate_phrases:
		# candidate_pinyin = pinyin.get(candidate_phrase, format="strip", delimiter="/").encode("utf-8")
		candidate_pinyin = pinyin.get(candidate_phrase, format="strip", delimiter="/")
		# 第一梯队 拼音相同
		if candidate_pinyin == error_pinyin:
			candidates_1st_order.append(candidate_phrase)
		# 第二梯队 第一个字拼音相同
		elif candidate_pinyin.split("/")[0] == error_pinyin.split("/")[0]:
			candidates_2nd_order.append(candidate_phrase)
		# 其他 第三梯队
		else:
			candidates_3nd_order.append(candidate_phrase)
	# print('c1_order is : ', candidates_1st_order)
	# print('c2_order is : ', candidates_2nd_order)
	# print('c3_order is : ', candidates_3nd_order)
	return candidates_1st_order, candidates_2nd_order, candidates_3nd_order


def auto_correct( error_phrase ):
	
	c1_order, c2_order, c3_order = get_candidates(error_phrase)
	# print c1_order, c2_order, c3_order
	if c1_order:
		return max(c1_order, key=phrase_freq.get )
	elif c2_order:
		return max(c2_order, key=phrase_freq.get )
	else:
		return max(c3_order, key=phrase_freq.get )

def auto_correct_sentence( error_sentence, verbose=True):
	
	# jieba_cut = jieba.cut( error_sentence.decode("utf-8"), cut_all=False)
	jieba_cut = jieba.cut(error_sentence, cut_all=False)
	# print('jieba_cut is : ',jieba_cut)
	seg_list = "\t".join(jieba_cut).split("\t")
	# print('seg_list is : ', seg_list)
	correct_sentence = ""
	n = 0
	for phrase in seg_list:
		
		correct_phrase = phrase
		# check if item is a punctuation
# 		if phrase not in PUNCTUATION_LIST.decode("utf-8"):
		if phrase not in PUNCTUATION_LIST:
			# check if the phrase in our dict, if not then it is a misspelled phrase
			# if phrase.encode("utf-8") not in phrase_freq.keys():
			if phrase not in phrase_freq.keys():
				# print('there is a misspelled phrase : ',phrase)
				# correct_phrase = auto_correct(phrase.encode("utf-8"))
				# find correct phrase
				correct_phrase = auto_correct(phrase)
				if verbose :
					print('\t', phrase)
					n = n + 1
	
		correct_sentence += correct_phrase
	return correct_sentence,n



phrase_freq = construct_dict( FILE_PATH )

# def main():
#
# 	err_sent_1 = '机七学习是人工智能领遇最能体现智能的一个分知！'
# 	print("Test case 1:")
# 	correct_sent = auto_correct_sentence( err_sent_1 )
# 	print("original sentence:" + err_sent_1 + "\n==>\n" + "corrected sentence:" + correct_sent)
#
# 	err_sent_2 = '杭洲是中国的八大古都之一，因风景锈丽，享有"人间天棠"的美誉！'
# 	print("Test case 2:")
# 	correct_sent = auto_correct_sentence( err_sent_2 )
# 	print("original sentence:" + err_sent_2 + "\n==>\n" + "corrected sentence:" + correct_sent)
#
# if __name__=="__main__":
# 	reload(sys)
# 	sys.setdefaultencoding('utf-8')
# 	main()


# candidate_phrases = pinyin.list( known(edits1(error_phrase, cn_words_dict)) )
candidate_phrases = construct_dict('./dict/token_freq_pos%40350k_jieba.txt').keys()
for candidate_phrase in candidate_phrases:
	candidate_phrase = pinyin.get(candidate_phrase, format="strip", delimiter="/")
# print('candidate_phrases is : ', candidate_phrases)

def get_wave_wrong(text):
	correct_sent, n = auto_correct_sentence(text)
	return n

# err_sent_1 = '机七学习是人工智能领遇最能体现智能的一个分知！'
# print("Test case 1:")
# correct_sent,n1 = auto_correct_sentence( err_sent_1 )
# print("original sentence:" + err_sent_1 + "\n==>\n" + "corrected sentence:" + correct_sent)
# print(n1)
# err_sent_2 = '杭洲是中国的八大古都之一，因风景锈丽，享有"人间天棠"的美誉！'
# print("Test case 2:")
# correct_sent,n2 = auto_correct_sentence( err_sent_2 )
# print("original sentence:" + err_sent_2 + "\n==>\n" + "corrected sentence:" + correct_sent)
# print(n2)
