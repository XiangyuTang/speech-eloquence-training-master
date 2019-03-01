import jieba


def getStopTime(text):
    stop_time = 0
    for t in text:
        if t == '额' or t == '嗯' or t == '呃' or t == '啊' or t == '唔':
            stop_time = stop_time + 1
    getSentence(text)
    return stop_time

def getSentence(text):
    jieba_cuts= jieba.cut(text, cut_all=False)
    cuts = []
    for jieba_cut in jieba_cuts:
        cuts.append(jieba_cut)
    for cut in cuts:
        if cut == '额' or cut == '嗯' or cut == '呃' or cut == '啊' or cut == '唔':
            # print(cuts.index(cut))
            if cuts.index(cut) >= 1 and cuts.index(cut) < len(cuts)-1:
                print('\t', cuts[cuts.index(cut)-2],cuts[cuts.index(cut)-1],cuts[cuts.index(cut)+1],cuts[cuts.index(cut)+2])

def realText(text):
    jieba_cuts = jieba.cut(text, cut_all=False)
    real_text = ''
    for cut in jieba_cuts:
        if cut == '额' or cut == '嗯' or cut == '呃' or cut == '啊' or cut == '唔':
            continue
        else:
            real_text += cut
    return real_text