import numpy as np
import wave
import platform as plat

def get_wav_list(filename):
    # 读取一个wav文件列表，返回一个存储该列表的字典类型值
    # ps:在数据中专门有几个文件用于存放用于训练、验证和测试的wav文件列表
    txt_obj = open(filename, 'r')  # 打开文件并读入
    txt_text = txt_obj.read()
    txt_lines = txt_text.split('\n')  # 文本分割
    dic_filelist = {}  # 初始化字典
    list_wavmark = []  # 初始化wav列表
    for i in txt_lines:
        if i != '':
            txt_l = i.split(' ')
            dic_filelist[txt_l[0]] = txt_l[1]
            list_wavmark.append(txt_l[0])
    txt_obj.close()
    return dic_filelist, list_wavmark


def get_wav_symbol(filename):
    # 读取指定数据集中，所有wav文件对应的语音符号
    # 返回一个存储符号集的字典类型值
    txt_obj = open(filename, 'r')
    txt_text = txt_obj.read()
    txt_lines = txt_text.split('\n')  # 文本分割
    dic_symbol_list = {}  # 初始化字典
    list_symbolmark = []  # 初始化symbol列表
    for i in txt_lines:
        if i != '':
            txt_l = i.split(' ')
            dic_symbol_list[txt_l[0]] = txt_l[1:]
            list_symbolmark.append(txt_l[0])
    txt_obj.close()
    return dic_symbol_list, list_symbolmark


def read_wav_data(filename):
    # 读取一个wav文件，返回声音信号的时域谱矩阵和播放时间
    wav = wave.open(filename, "rb")  # 打开一个wav格式的声音文件流
    num_frame = wav.getnframes()  # 获取帧数
    num_channel = wav.getnchannels()  # 获取声道数
    framerate = wav.getframerate()  # 获取帧速率
    num_sample_width = wav.getsampwidth()  # 获取实例的比特宽度，即每一帧的字节数
    str_data = wav.readframes(num_frame)  # 读取全部的帧
    wav.close()  # 关闭流
    wave_data = np.fromstring(str_data, dtype=np.short)  # 将声音文件数据转换为数组矩阵形式
    wave_data.shape = -1, num_channel  # 按照声道数将数组整形，单声道时候是一列数组，双声道时候是两列的矩阵
    wave_data = wave_data.T  # 将矩阵转置
    # wave_data = wave_data
    return wave_data, framerate


def GetFrequencyFeature3(wavsignal, fs):
    # wav波形 加时间窗以及时移10ms
    time_window = 25  # 单位ms
    window_length = fs / 1000 * time_window  # 计算窗长度的公式，目前全部为400固定值

    wav_arr = np.array(wavsignal)
    # wav_length = len(wavsignal[0])
    wav_length = wav_arr.shape[1]

    range0_end = int(len(wavsignal[0]) / fs * 1000 - time_window) // 10  # 计算循环终止的位置，也就是最终生成的窗数
    data_input = np.zeros((range0_end, 200), dtype=np.float)  # 用于存放最终的频率特征数据
    data_line = np.zeros((1, 400), dtype=np.float)
    for i in range(0, range0_end):
        p_start = i * 160
        p_end = p_start + 400

        data_line = wav_arr[0, p_start:p_end]

        x = np.linspace(0, 400 - 1, 400, dtype=np.int64)
        w = 0.54 - 0.46 * np.cos(2 * np.pi * (x) / (400 - 1))  # 汉明窗
        data_line = data_line * w  # 加窗

        data_line = np.abs(np.fft(data_line)) / wav_length

        data_input[i] = data_line[0:200]  # 设置为400除以2的值（即200）是取一半数据，因为是对称的

    # print(data_input.shape)
    data_input = np.log(data_input + 1)
    return data_input


def GetData(self, n_start, n_amount=1):
    # 读取数据，返回神经网络输入值和输出值矩阵(可直接用于神经网络训练的那种)
    # 参数：
    #    n_start：从编号为n_start数据开始选取数据
    #    n_amount：选取的数据数量，默认为1，即一次一个wav文件
    # 返回：
    #    三个包含wav特征矩阵的神经网络输入值，和一个标定的类别矩阵神经网络输出值

    # 当为test or valid 时随机选择thchs30或者st-cmd数据集中的语音数据
    bili = 2
    # 当为train时，由于st-cmd数据是thchs30数据的10倍，因此设置bili=11使得两个数据集的数据分布相同。
    if (self.type == 'train'):
        bili = 11

    # 读取一个文件
    if (n_start % bili == 0):
        filename = self.dic_wavlist_thchs30[self.list_wavnum_thchs30[n_start // bili]]
        list_symbol = self.dic_symbollist_thchs30[self.list_symbolnum_thchs30[n_start // bili]]
    else:
        n = n_start // bili * (bili - 1)
        yushu = n_start % bili
        length = len(self.list_wavnum_stcmds)
        filename = self.dic_wavlist_stcmds[self.list_wavnum_stcmds[(n + yushu - 1) % length]]
        list_symbol = self.dic_symbollist_stcmds[self.list_symbolnum_stcmds[(n + yushu - 1) % length]]

    if ('Windows' == plat.system()):
        filename = filename.replace('/', '\\')  # windows系统下需要执行这一行，对文件路径做特别处理

    wavsignal, fs = read_wav_data(self.datapath + filename)

    # 获取输出特征

    feat_out = []
    print("数据编号", n_start, filename)
    for i in list_symbol:
        if ('' != i):
            n = self.SymbolToNum(i)
            # v=self.NumToVector(n)
            # feat_out.append(v)
            feat_out.append(n)
    print('feat_out:', feat_out)

    # 获取输入特征
    data_input = GetFrequencyFeature3(wavsignal, fs)
    # data_input = np.array(data_input)
    data_input = data_input.reshape(data_input.shape[0], data_input.shape[1], 1)
    # arr_zero = np.zeros((1, 39), dtype=np.int16) #一个全是0的行向量

    # while(len(data_input)<1600): #长度不够时补全到1600
    #	data_input = np.row_stack((data_input,arr_zero))

    # data_input = data_input.T
    data_label = np.array(feat_out)
    return data_input, data_label

