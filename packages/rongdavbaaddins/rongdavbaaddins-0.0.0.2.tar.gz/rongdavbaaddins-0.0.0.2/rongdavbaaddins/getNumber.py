import sys

import requests
import time
import random
import sys

def GetFunNum(functionName, token):
    url = f'http://39.102.142.236:19518/vadmin/auth/GetFuncitonNum'
    # url = f'http://39.107.28.207:9000/vadmin/auth/GetFuncitonNum'

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Authorization": f"bearer {token}",
        'Connection': 'keep-alive',
        'Cookie': 'jenkins-timestamper-offset=-28800000',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0"

    }
    data = {
        "function": functionName
    }
    response = requests.post(url, headers=headers, params=data)
    print(response.text)
    if response.status_code != 200:
        num = 0
        while num < 3:
            time.sleep(random.uniform(0.5, 1))
            response = requests.post(url=url, headers=headers)
            if response.status_code == 200:
                if response.json()["code"] == 200:
                    # 返回数量
                    # return response.json()['data']
                    print(response.json()['data'])
            if num == 2:
                print(-1)
            num += 1
    elif response.status_code == 200:
        if response.json()["code"] == 200:
            print(response.json()['data'])
        else:
            print(-1)
    else:
        print(-1)

if __name__ == "__main__":
    # functionName = "OCR"
    functionName = "rongdavbaaddins"
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAyODEzIiwiaXAiOiIxNzIuMTYuNzMuMSIsIm1hYyI6IjAwMmI2N2UyMmQ1OCJ9.AodD4YiUvl6rVdY0xk3ExnRMVSNxwx0un3vyjZWVDcU'
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwiaXAiOiIxOTIuMTY4LjExLjEyNCIsIm1hYyI6ImUwMGFmNmE3YmJmYSJ9.7Mq_mIrVqH22Sj_gkduhA0N0aqYDyifECC4XJ-H4bEY'
    # functionName = sys.argv[1]
    #9000服务器
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAyODEzIiwiaXAiOiIxNzIuMTYuNzMuMSIsIm1hYyI6IjAwMmI2N2UyMmQ1OCJ9.AodD4YiUvl6rVdY0xk3ExnRMVSNxwx0un3vyjZWVDcU'
    # token = sys.argv[2]
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwiaXAiOiIxOTIuMTY4LjExLjEyNCIsIm1hYyI6ImUwMGFmNmE3YmJmYSJ9.7Mq_mIrVqH22Sj_gkduhA0N0aqYDyifECC4XJ-H4bEY'
    GetFunNum(functionName, token)