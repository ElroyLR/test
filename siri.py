@@ -0,0 +1,103 @@
import urllib.parse
import hashlib
import time
import random
import string
import requests
import sys
import readline

def curl_md5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()


"""
get_req_sign ：根据 接口请求参数 和 应用密钥 计算 请求签名
参数说明
    -pa：接口请求参数
    -apk：应用密钥
返回数据
    -签名结果
"""


def get_req_sign(pa, apk):

    # 1.字典升序排序
    pa_list = list(pa.items())
    pa_list.sort()

    # 2.拼按URL键值对
    tem_str = ''
    for i in range(len(pa_list)):
        if pa_list[i][1]:
            tem_str += (pa_list[i][0] + '=' + urllib.parse.quote(pa_list[i][1]) + '&')

    # 3.拼接app_key
    tem_str += ('app_key=' + apk)

    # 4.MD5运算 + 转换大写，得到请求签名
    sign = curl_md5(tem_str)
    return sign


def get_params(plus_item):

    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效） 
    t = time.time()
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))

    global se

    app_id = '2127007340'
    app_key = '9Fm2D9tkB4lEjZ89'
    params = {
        'app_id': app_id,
        'time_stamp': time_stamp,
        'nonce_str': nonce_str,
        'question': plus_item,
        'sign': '',
        'session': se
    }

    params['sign'] = get_req_sign(params, app_key)
    return params


def get_content(plus_item):
    # 聊天的API地址    
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    # 获取请求参数  
    plus_item = plus_item.encode('UTF-8')
    payload = get_params(plus_item)
    r = requests.post(url, data=payload)

    if r.json()["ret"] == 0:
        print('吴小枫：' + r.json()["data"]["answer"])
    else:
        print('今天我出了一点小问题~快联系助教帮忙解决一下~~')
        sys.exit()


feature_text = ['''
大家好！我是你的聊天机器人吴小枫。
我有问必答，有人会问我“今天深圳天气怎么样？”，也有人问我“你喜欢我吗？”
快来问我问题呀，欢迎来撩！
>''', '''
再来问我点啥吧！我把我知道的都告诉你，嘻嘻！
>''', '''
# 我有点饿了，再和你聊完最后一句，我就要下线啦！你还有什么要问我的？
# >''']

se = str(random.randint(1, 10000))

for i in range(len(feature_text)):
    comment = input(feature_text[i])
    get_content(comment)
    time.sleep(1)

print('\n我走啦，下次见！')
