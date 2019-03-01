import emotion
import tone
import accurate
import advice
import fluency
import trans
import numpy

filename = 'sample.wav'
text = trans.tanslateIntoText(filename)
print('=======================================演讲稿生成=======================================')

# real_text = fluency.realText(text)
# print('\t', real_text)
print('\t', text)

print('========================================语速分析========================================')
text_len = len(text)
print('该次演讲字数为：', text_len, '字；')

time, snd, p = tone.get_wav_A(filename)
print('演讲时间为：', time/1000, '秒；')

speed = text_len / time * 1000 * 60
print('总体语速为：', speed, '字/分钟；')

# print('我们推荐的语速为 150字/分钟。')

print('=======================================流畅度分析=======================================')

print('以下为您演讲不流利之处：')

stop_time = 0

stop_time = fluency.getStopTime(text)
if stop_time == 0:
    print('\t无')

print('您一共停顿了', stop_time, '次')

print('=======================================准确度分析=======================================')

wrong_time = 0

print('以下为您发音不标准之处：')

wrong_time = accurate.get_wave_wrong(text)
if wrong_time == 0:
    print('\t无')

print('您一共有', wrong_time, '处发音不准确')

print('========================================情感分析========================================')
emotion_S = []
# averageP, averageSnd, minSnd, maxSnd, varSnd
textLists = text.split('。')
i = 0
total = len(textLists)
for textList in textLists:
    if textList != '':
        i += 1
        score = emotion.getTextEmotion(textList)
        print(textList, '\n\t本句话的感情色彩强度应为：', abs(score))
        realscore = emotion.getWaveEmotion(i, total, snd, p, time, len(textLists))
        print('\t您演讲的感情色彩强度为：', abs(realscore))
        emotion_S .append(abs(abs(score) - abs(realscore)))
S = numpy.sum(emotion_S) / total


print('==========================================总分==========================================')
score = advice.calculateScore(speed, stop_time, wrong_time, S)
print('您的总分为：', score, '分')
# print('改进意见如下：')
