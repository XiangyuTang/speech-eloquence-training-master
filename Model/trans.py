from aip import AipSpeech


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件


def tanslateIntoText(filename):
    """ 你的 APPID AK SK """
    APP_ID = '15641939'
    API_KEY = 'IpaEj0GRHd1PhyZNQiWDjrRl'
    SECRET_KEY = 'NWsYD2PQXX9VRVOoVZ77PVMyVWfaBzFe'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # print(get_file_content(filename))

    k = client.asr(get_file_content(filename), 'pcm', 16000, {
        'dev_pid': 1536,
    })
    # print(k)
    str1 = str(k['result'])
    str2 = str1[2:-2]
    return str2
#
# str = tanslateIntoText('a.wav')
# print(str)
# tanslateIntoText('Rec 0002.wav')