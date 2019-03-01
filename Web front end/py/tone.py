import pylab as pl
from scipy.io import wavfile
import numpy as np


def get_wav_L(filename):
    sampFreq, snd = wavfile.read(filename)
    # 声压值归一化，映射到区间[-1, 1)
    snd = snd / (2. ** 15)
    # 计算采样点数
    point = snd.shape[0]
    # 计算语音时长length，单位秒，例如cafe.wav中时长为300004.0ms（5分钟300秒）
    length = snd.shape[0] / sampFreq
    return length


# 输入音频名，返回音频时长，强度，平均振幅，最小振幅，最大振幅，基频振幅
def get_wav_A(filename):
    sampFreq, snd = wavfile.read(filename)
    # 声压值归一化，映射到区间[-1, 1)
    snd = snd / (2.**15)
    # 计算采样点数
    point = snd.shape[0]
    # 计算语音时长length，单位毫秒，例如cafe.wav中时长为300004.0ms（5分钟300秒）
    ###############################################################################################
    length = snd.shape[0] * 1000 / sampFreq
    ###############################################################################################
    # 计算需要返回的四个基频数据
    # ###############################################################################################
    # maxSnd = np.max(abs(snd))
    # minSnd = np.min(abs(snd))
    # averageSnd = np.average(abs(snd))
    # varSnd = np.var(abs(snd))
    # ###############################################################################################
    # # 创建时间点数组
    # timeArray = pl.arange(0, point, 1)   #[0s, 1s], 采样点数个点，cafe中为4800064个点
    # timeArray = timeArray / sampFreq   #[0s, 300s]
    # timeArray = timeArray * 1000       #[0ms, 300004.0ms]
    # # 绘图
    # pl.plot(timeArray, snd, color='k')
    # pl.ylabel('Amplitude')
    # pl.xlabel('Time (ms)')
    # pl.show()

    n = len(snd)
    p = pl.fft(snd)         #执行傅立叶变换
    nUniquePts = int(pl.ceil((n+1)/2.0))
    p = p[0:nUniquePts]
    p = abs(p)
    p = p / float(n)    #除以采样点数，去除幅度对信号长度或采样频率的依赖
    p = p**2            #求平方得到能量

    if n % 2 > 0:       #fft点数为奇
        p[1:len(p)] = p[1:len(p)]*2
    else:               #fft点数为偶
        p[1:len(p)-1] = p[1:len(p)-1] * 2

    # freqArray = pl.arange(0, nUniquePts, 1.0) * (sampFreq / n)
    # pl.plot(freqArray, p, color='k')
    # pl.xlabel('Freqency (Hz)')
    # pl.ylabel('Power (dB)')
    # pl.show()
    # print(pl.sqrt(pl.mean(snd**2)))
    # print(pl.sqrt(sum(p)))
    ###############################################################################################
    # 强度用总能量的平方根 / 时长 表示
    averageP = pl.sqrt(sum(p)) / length
    ###############################################################################################
    # print("文件名称：" + filename)
    # print("音频时长：" + str(length))
    # print("音频强度：" + str(averageP))
    # print("平均振幅：" + str(averageSnd))
    # print("最小振幅：" + str(minSnd))
    # print("最大振幅：" + str(maxSnd))
    # print("振幅变化：" + str(varSnd))

    # return length, averageP, averageSnd, minSnd, maxSnd, varSnd
    # return length

    # print('p is : ', p)
    # print('snd is : ', snd)
    return length, snd, p

# 输入文件名，返回平均基频，最小基频，最大基频，基频变化
def get_wav_f(filename):
    averageSnd = 0
    maxSnd = 0
    minSnd = 0
    varSnd = 0
    print("文件名称：" + filename)
    print("平均基频：" + str(averageSnd))
    print("最小基频：" + str(minSnd))
    print("最大基频：" + str(maxSnd))
    print("基频变化：" + str(varSnd))
    return averageSnd, minSnd, maxSnd, varSnd

# get_wav_A(filename)
# get_wav_f(filename)
