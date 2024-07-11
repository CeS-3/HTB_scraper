# -*- coding: utf-8 -*-

import requests
import json
import time
from dao import database  # 确保正确导入database类
from datetime import datetime


# 定义请求头
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    # Authorization 需要更新
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI2IiwianRpIjoiZmY0MDY4ZGNmZGU0NDgxNDEyMjFhODMzNzhhYTYwYjZiMDE0YmI1N2MxNzYzNmJiY2ZhOGIwMWJmMDAyOWU1Y2EyYTU0Y2UzZDUwZGYxM2IiLCJpYXQiOjE3MjA2MTE1NTUuNTQ4MTM4LCJuYmYiOjE3MjA2MTE1NTUuNTQ4MTQsImV4cCI6MTcyMDY5Nzk1NS41NDAzMDUsInN1YiI6IjIwMDYyMjYiLCJzY29wZXMiOltdfQ.g9o7HPP42MQ4OdEWFi0ZWAHTv6K9FKp_MIM7d20Fo530Sv1JhwrzM25NksXs1Qer2yDBoB3-uNJDmRp9dNjbDxSJk1QqJ8IG1nDu_HSn1DKGwyx5uPrIjOX_0aOEovf-EUmp3nA88KucVO_dRl_7GW5SSN1C3VX8IiPWRiH4TnJS6ZeGqGAKTfGPMPvNrD4tEjm8z_w-bamyI-8mXPxz-dTlruY1weRuOROGQxCzPSIWQvQU2zyFTQi6MSs_pD3HVtZAGmeYRGwz2pu-iHjbApUQanzNKOgt4T9S5BTr4FB6pLetVyfbQgKei7wOhZDxpD9obSmWxK9ZYGR7eH9GN33l6M9LGzcjedPZ4YHQbqReHZe3CKc5HKTaOkNqa-2cyy3Z8tzw8QQq0ImBl2xodzxTXrEk9NXTvlePwi4wY75dRo-EAXU7mQfBr1XjG6wLGyv7jSOkP2oFwW6S8bX6QyLUoFcBwhypyLhVfmiVXZjidDIUYK518rRU0dvPeznfqhmKLErI34j_xUXVYMQjvAEpGhE4qvXB7GWF4xb6HKXq43jcsleCVg5SuWQbXmVBm890NCGMRaerWIUxD9usip3u2BsZbbYvuorLfD4DqS1MhCUh14VJXPk7OM2dcPgO2yaqesgnfyApBSrJfQ4FIIQ-jor9SaUXfV2Nn5_3WuM",
    "Referer": "https://app.hackthebox.com/",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
}

# API的url
url_dict = {
    "graph_url": "https://labs.hackthebox.com/api/v4/user/profile/graph/1Y/",
    "machine_attack_url": "https://labs.hackthebox.com/api/v4/user/profile/chart/machines/attack/",
    "machine_os_url": "https://labs.hackthebox.com/api/v4/user/profile/progress/machines/os/",
    "challenge_url": "https://labs.hackthebox.com/api/v4/user/profile/progress/challenges/",
    "sherlock_url": "https://labs.hackthebox.com/api/v4/user/profile/progress/sherlocks/",
    "user_info_url": "https://labs.hackthebox.com/api/v4/user/profile/basic/"
}

def get_new_Token():
    new_Token = input("请输入新的Token值:")
    headers["Authorization"] = new_Token
    print("token更换成功")
# 爬取数据
flag = True
start_time = time.time()

db = database(prefix="hackthebox")

with open("user_id.txt", "r") as user_ids:
    for user_id in user_ids:
        user_id = user_id.strip()  # 去除换行符和空格
        if db.if_exist(user_id):
            print(f"用户 {user_id} 已存在，pass")
            continue

        user_data = []

        for url in url_dict.values():
            full_url = url + user_id
            while True:
                #发送请求
                response = requests.get(full_url, headers=headers)
                #若请求成功
                if response.status_code == 200:
                    #插入该项
                    data = response.json()
                    user_data.append(data)
                    print(".", end='')
                    #离开该死循环
                    break
                elif response.status_code == 401:
                    #若token过期
                    print("Token过期,换一个")
                    #请求一个新的token
                    get_new_Token()
                    time.sleep(0.75)
                    #此处不离开死循环，再进行一次请求
                else:
                    print(f"被封了,响应码:{response.status_code}")
                    flag = False
                    #若ip被封
                    #直接离开死循环
                    break
            if not flag:
                break 
            time.sleep(0.75)

        if not flag:
            break
        db.insert_user_data(user_id, user_data)
        print(f"用户 {user_id} 爬取完成")

end_time = time.time()
sum_time = end_time - start_time

if flag:
    print(f"所有用户信息爬取完成")
    #获取当前时间
    now = datetime.now()
    # 格式化日期和时间
    formatted_datetime = now.strftime("%Y-%m-%d-%H:%M:%S")
    db.export_and_del(export_path=f"user_info-{formatted_datetime}.json")
    print(f"爬取完成，当前轮次耗时{sum_time}秒")
else:
    print(f"爬取异常终止，当前轮次耗时{sum_time}秒")
