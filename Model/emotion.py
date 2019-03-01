from collections import defaultdict
import os
import re
import jieba
import codecs
import numpy as np


# 分词，去除停用词
def sent2word(sentence):
    segList = jieba.cut(sentence)
    segResult = []
    for w in segList:
        segResult.append(w)

    txt_obj = open('./dict/stop_words.txt', 'r', encoding = 'UTF-8')  # 打开文件并读入
    txt_text = txt_obj.read()
    txt_lines = txt_text.split('\n')  # 文本分割
    wordDict = defaultdict()
    wordList = []
    i = 0
    for word in segResult:
        if word in txt_lines:
            # print "stopword: %s" % word
            continue
        else:
            # 列表转为字典
            if word not in wordDict.keys():
                wordList.append(word)
                wordDict[word] = i
                i = i+1

    return wordList, wordDict

# 将各类词分为情感词、否定词、程度副词，并记录其位置
def classifyWords(wordDict):
    # (1) 情感词
    f1 = open('./dict/BosonNLP_sentiment_score.txt', 'r', encoding='UTF-8')  # 打开文件并读入
    senList = f1.readlines()
    senDict = defaultdict()
    for s in senList:
        senDict[s.split(' ')[0]] = s.split(' ')[1]
    # (2) 否定词
    f2 = open('./dict/notDict.txt', 'r', encoding='UTF-8')  # 打开文件并读入
    notList = f2.readlines()
    # (3) 程度副词
    f3 = open('./dict/degreeDict.txt', 'r', encoding='UTF-8')  # 打开文件并读入
    degreeList = f3.readlines()
    degreeDict = defaultdict()
    for d in degreeList:
        degreeDict[d.split(' ')[0]] = d.split(' ')[1]

    senWord = defaultdict() #情感词
    notWord = defaultdict() #否定词
    degreeWord = defaultdict() #程度副词

    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys(): #是情感词
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys(): #是否定词
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys(): #是程度副词
            degreeWord[wordDict[word]] = degreeDict[word]
    return senWord, notWord, degreeWord


def scoreSent(senWord, notWord, degreeWord, segResult, d):
    W = 1
    score = 0
    # 存所有情感词的位置的列表
    senLoc = senWord.keys()
    notLoc = notWord.keys()
    degreeLoc = degreeWord.keys()
    senloc = -1
    # notloc = -1
    # degreeloc = -1

    # 遍历句中所有单词segResult，i为单词绝对位置
    for i in range(0, len(segResult)):
        # 如果该词为情感词
        if i in senLoc:
            # loc为情感词位置列表的序号
            senloc += 1
            # 直接添加该情感词分数
            score += W * float(senWord[i])
            # print "score = %f" % score
            # print(score)
            if senloc < len(senLoc) - 1:
                # 判断该情感词与下一情感词之间是否有否定词或程度副词
                # j为绝对位置
                for j in range(d[segResult[senloc]], d[segResult[senloc + 1]]):
                    # 如果有否定词
                    if j in notLoc:
                        W *= -1
                    # 如果有程度副词
                    elif j in degreeLoc:
                        W *= float(degreeWord[j])
        # i定位至下一个情感词
        # if senloc < len(senLoc) - 1:
        #     i = senLoc[senloc + 1]
    return score

def getTextEmotion(text):
    wordList, wordDict = sent2word(text)
    # print(wordList)
    # print(wordDict)
    senWord, notWord, degreeWord = classifyWords(wordDict)
    # print(senWord)
    # print(notWord)
    # print(degreeWord)
    # print(wordList)
    score = scoreSent(senWord, notWord, degreeWord, wordList, wordDict)
    # print('本句话的感情色彩强度应为：', abs(score))
    return score

def getWaveEmotion(i, total, snd, p, length, n):
    l = (int)(np.ceil(len(snd) / n) - 1)
    start = l * (i - 1)
    end = start + l
    snd2 = snd[start:end]
    averageP = np.sqrt(sum(p)) / length
    maxSnd = np.max(abs(snd2))
    minSnd = np.min(abs(snd2))
    averageSnd = np.average(abs(snd2))
    varSnd = np.var(abs(snd2))
    # print('averageP : ', averageP)
    # print('maxSnd  : ', maxSnd )
    # print('minSnd : ', minSnd)
    # print('averageSnd : ', averageSnd)
    # print('varSnd : ', varSnd)

    score = averageP * 50000 + (maxSnd - minSnd) + 2 * averageSnd + varSnd

    return score