import sys

import requests
import time
import random
import sys

def minusFunction(functionName, token):
    # url = f'http://39.102.142.236:19518/vadmin/auth/rongdavbaaddins'
    url = 'http://39.102.142.236:19518/vadmin/auth/minusFunction'
    headers = {
        "Authorization": f"bearer {token}",
        'Cookie': 'jenkins-timestamper-offset=-28800000',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    data = {
        "function": functionName,
        'num' : 10
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
    functionName = "OCR"
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAyODEzIiwiaXAiOiIxNzIuMTYuNzMuMSIsIm1hYyI6IjAwMmI2N2UyMmQ1OCJ9.AodD4YiUvl6rVdY0xk3ExnRMVSNxwx0un3vyjZWVDcU'
    # functionName = sys.argv[1]
    # token = sys.argv[2]
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwiaXAiOiIxNzIuMTYuNzMuMSIsIm1hYyI6IjAwMmI2N2UyMmQ1OCJ9.nuphngVh-HEXUhQeiADFvvEOKMwASpCFxWb2VtC0AH4'
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlwIjoiMTcyLjE2LjczLjEiLCJtYWMiOiIwMDJiNjdlMjJkNTgifQ.MU46YMN6XTcsIIUf6KsjuhcKlleQ8_56rCx0YfMuNIE'
    minusFunction(functionName, token)