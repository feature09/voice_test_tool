# -*- coding: utf-8 -*-
# @Time     :2019/2/25
# @Author   :qpf


from aip import AipSpeech
import urllib.request
import urllib.parse
import time
import urllib
import json
import hashlib
import base64


# 百度
def get_data(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


def asr_baidu(file_path):
    APP_ID = get_args()['APP_ID']
    API_KEY = get_args()['API_KEY']
    SECRET_KEY = get_args()['SECRET_KEY']
    try:
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        ret = client.asr(get_data(file_path), 'pcm', 16000, {'dev_pid': 1536}, )
        # print(ret)  # test
        return ret['result']
    except Exception as e:
        # print(e)  # test
        return ['error-语音识别错误']


# 科大讯飞
def asr_kdxf(AUDIO_PATH):
    f = open(AUDIO_PATH, 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.parse.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    x_appid = get_args()['x_appid']
    api_key = get_args()['api_key']
    param = {"engine_type": "sms16k", "aue": "raw"}

    json_str = json.dumps(param).replace(' ', '')
    x_param = base64.b64encode(bytes(json_str, 'ascii'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    combine_all = api_key + str(x_time) + str(x_param)[2:-1]
    x_checksum = hashlib.md5(combine_all.encode(encoding='utf-8')).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, bytes(body, 'ascii'), x_header)
    result = urllib.request.urlopen(req)
    result = eval(result.read())
    # print(result) # test
    output_result = result['data']
    if output_result == '':
        return ['error-语音识别错误']
    else:
        return [output_result]


def main(choice=1):
    audio_path = get_args()['audio_path']
    if choice == 1:
        asr = asr_baidu(audio_path)
    elif choice == 2:
        asr = asr_kdxf(audio_path)
    else:
        asr = ['error-语音识别选择错误']
    return asr


def get_args():
    args = {}
    with open('args.txt', 'r', encoding='utf-8') as atr:
        lines = atr.readlines()
        for line in lines:
            head = line.replace('\n', '').split('=')[0]
            value = line.replace('\n', '').split('=')[1]
            args[head] = value
    return args


if __name__ == '__main__':
    print(main(choice=1)[0])
    print(get_args())
