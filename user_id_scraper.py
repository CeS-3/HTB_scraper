# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Authorization": "",
    "Origin": "https://app.hackthebox.com",
    "Referer": "https://app.hackthebox.com/",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
}
file_path = "user_id.txt"

def get_user_id_in_rankings_page(file_path):
    url = "https://labs.hackthebox.com/api/v4/rankings/users"
    response = requests.get(url, headers=headers)
    with open(file_path,'w') as file:
        # 检查响应状态码
        if response.status_code == 200:
            data = response.json()
            num = len(data["data"])
            print(f"获取到{num}条用户信息")
            for user_info in data["data"]:
                user_id = user_info["id"]
                file.write(str(user_id) + "\n")
        else:
            print(f"请求失败，状态码: {response.status_code}")


def get_user_id_in_database(page_num,file_path):
    with open(file_path,'w') as file:
        for num in range(1,page_num + 1):
            database_url = f"https://labs.hackthebox.com/api/v4/players/fetch_data?page={num}"
            response = requests.get(url=database_url,headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content,"html.parser")
                id_elements = soup.select("p.font-size13.line-height-18.mb-0")
                for id_element in id_elements:
                    file.write(id_element.text.replace("#","").strip() + "\n")
                print(f"第{num}页爬取完成")
            else:
                print(f"请求失败，状态码: {response.status_code}") 
            time.sleep(1)

page_num = 1500

get_user_id_in_database(page_num,file_path)