# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import re
import sys
import time

import requests
from Crypto.Cipher import AES
from requests.structures import CaseInsensitiveDict

header = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;zfsoft',
}


def cbc_encrypt(plaintext: str) -> str:
    """
    AES-CBC 加密
    key 必须是 16(AES-128)、24(AES-192) 或 32(AES-256) 字节的 AES 密钥；
    初始化向量 iv 为随机的 16 位字符串 (必须是16位)，
    解密需要用到这个相同的 iv，因此将它包含在密文的开头。
    """
    key = 'ED7925CF8acd26B0'
    block_size = len(key)
    padding = (block_size - len(plaintext) % block_size) or block_size  # 填充字节

    iv = '3670759D768a359f'
    mode = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    ciphertext = mode.encrypt((plaintext + padding * chr(padding)).encode())

    return ciphertext.hex()


def cbc_decrypt(ciphertext: str) -> str:
    """
    AES-CBC 解密
    密文的前 16 个字节为 iv
    """
    key = 'ED7925CF8acd26B0'
    iv = '3670759D768a359f'
    mode = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    plaintext = mode.decrypt(bytes.fromhex(ciphertext))
    return plaintext[:-plaintext[-1]].decode()


def check(username: str, password: str, location: str, coordinate: str) -> str:
    """
    进行一次报的送
    :param username: 学号
    :param password: 密码，教务网的
    :param location: 定位地址名，XX省XX市这样的
    :param coordinate: 经纬度，用英文逗号隔开
    :return: 返回报送信息，如果是代码层面监测到错误了，则开头必定为 !!! 三个感叹号
    """
    try:
        user = {
            "username": username,
            "password": password,
            "redirectUrl": "https://myapp.zjgsu.edu.cn/home/index",
            "clientId": "qnFZATsB6D25EnZeII",
            "mobileBT": "11111111-1111-1111-1111-111111111111"
        }
        s = requests.session()
        res = s.post('https://uia.zjgsu.edu.cn/cas/mobile/getAccessToken', data=user, headers=header)
        access_token = res.json()['access_token']
        s.get('https://uia.zjgsu.edu.cn/cas/login?service=https://myapp.zjgsu.edu.cn/home/index&access_token='
              + access_token + '&mobileBT=' + user['mobileBT'])

        res = s.get('https://ticket.zjgsu.edu.cn/stucheckservice/auth/login/stuCheck', headers=header)
        referer = res.history[-1].headers['location']
        token = re.search(R'\?token=(.+?)&', referer).group(1)
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + token
        headers["token"] = token
        headers["Content-Type"] = "application/json"
        if sys.argv[1] == 'ticket':
            data = """{"place": "浙江省,杭州市,钱塘区,学正街18号","coordinate": "120.388529,30.308752"}""".encode('utf-8')
            res = s.get('https://ticket.zjgsu.edu.cn/stucheckservice/service/getchecklist', headers=headers, data=data)
            if len(res.json()['data']['items']) > 0:
                return '主动报送'
            res = s.post('https://ticket.zjgsu.edu.cn/stucheckservice/service/stuclockin', headers=headers, data=data)
            return '成功打卡' if res.json()['code'] == 20000 else '!!!打卡失败!!!'
        elif sys.argv[1] == 'yzy':
            # 这里是新的两个参数的破解方案
            t = str(int(datetime.datetime.now().timestamp() * 1000))
            tp = t + '26B0'
            headers["zjgsuAuth"] = hashlib.md5((user['username'] + '*' + tp + '^25A622DCE625882D8085CC9F00BF8C12')
                                               .encode('utf-8')).hexdigest()
            headers['zjgsuCheck'] = cbc_encrypt('882D' + tp)

            data = {
                "currentResd": location,
                "fromHbToZj": "C",
                "fromWtToHz": "B",
                "meetCase": "C",
                "travelCase": "D",
                "medObsv": "B",
                "belowCase": "D",
                "hzQrCode": "A",
                "specialDesc": "无",
                "deviceId": "iPhone 104 pro max plus",
                "fromDevice": "WeChat",
                "isNewEpid": "否",
                "location": location,
                "coordinate": coordinate
            }
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            res = s.post('https://yzy.zjgsu.edu.cn/cloudbattleservice/service/add', headers=headers, data=data)
            msg = res.json()['message']
            return msg
        else:
            return '!!!参数错误!!!'
    except Exception as e:
        return '!!!出错导致打卡失败!!!'


if __name__ == '__main__':
    with open('app-user.json', encoding='utf-8') as f:
        users = json.load(f)
    for u in users:
        res = check(u['username'], u['password'], 'AB省CD市', '37.3346437,122.0131992')
        print(datetime.datetime.now().strftime('%Y-%m-%d'), res)
        time.sleep(10)
