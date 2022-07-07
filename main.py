# -*- coding: utf-8 -*-
import os
import datetime
import time
import json
from app import check
import sys

if __name__ == '__main__':
    sys.argv.append('yzy')
    users = str(os.environ["users"])
    users = json.loads(users)
    error_flag = False
    error_list = []
    for u in users:
        tmp = u['username']
        try:
            res = check(u['username'], u['password'], '浙江省杭州市', '120.389086,30.319279')
            if('成功' in res or '已打卡' in res):
                print(datetime.datetime.now().strftime('%Y-%m-%d'), tmp, res)
            else:
                error_flag = True
                error_list.append(tmp)
                print(datetime.datetime.now().strftime('%Y-%m-%d'), tmp, res)
        except:
            error_flag = True
            error_list.append(tmp)
            print(datetime.datetime.now().strftime('%Y-%m-%d'), tmp, '打卡失败！', res)
        time.sleep(10)
    if(error_flag):
        raise Exception('云签到打卡失败用户:{}'.format(str(error_list)))