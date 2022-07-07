# -*- coding: utf8 -*-
import os
import requests
s = requests.session()
token = str(os.environ["alive"])
headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'token {}'.format(token)}
url = 'https://api.github.com/repos/yujianke100/AFANZ/actions/workflows/main.yml/enable'
res = s.put(url, headers=headers)
if(res.status_code != 204):
    raise Exception('自动续杯失败！')
