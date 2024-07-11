# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI2IiwianRpIjoiOWY5OWExMjllYmRjNzMxYjY0ZTIyMjNiMDk1ZWYxZjk5MDRjOWIzMTFkMzZkZTg3OTU5Nzg5MjRlMjRlMmRmMzQwMWRkZTg1NzAwNzEwZGEiLCJpYXQiOjE3MjA1MjYyMDEuODk2NDY2LCJuYmYiOjE3MjA1MjYyMDEuODk2NDY5LCJleHAiOjE3MjA2MTI2MDEuODEyMzUyLCJzdWIiOiIyMDA2MjI2Iiwic2NvcGVzIjpbXX0.r0GTMO9edN_w89Ew8jXVyg20GMMVv4G_wA7lK00kPgw0563zzzmRfVgNdT3hMjL8EHfoiQDIsJMxKuwZlhG3__YC3uWacABnzKC9usANi8SHdLRd2wDmeA3lS4u8xLINNpKRCfQQhXJDgpDiVlsUmqJ2mmTtlDjftw8kCoqQptCh8ep82w0p94t4dHUGwCTg9Z2SgAlJJQtX6cFGCy6NmUXJmQMCqQXlqAyZYo2FvdkBGPRTpqxlQjXCdDumhLZfRfYI1EgcFk3nCwwfv08XYelc1_68tZ00BwKcP7y7UJUQGdF8aameNdlYxirkQZWA7S9ZO5WosZkb9YZk2mNpSNE-sqspDtNq_HFPPXc88S7S_Jb3Atm80vhcMmt8bFDoT1qMkVuUQVVnaoYqE-ec-hSKCuxxamYha3SMvmpfXy4kdc_q1wTVbf8va2g5Hh7Yo01FAm-dIlAWm43ujhKLHtZ2TNdgzVI_X0eUtD1iWLozzLkthinbfq2sS1Gb0YEUp8xMxuKT6uSXtqF34a9QYvqBRaWYAiTfPqMd0A1S9h2P43wb-Yvc_vYZ8HHfhIjW0fCykzo4YanbIGw89TAquCyePtE3aiNqOLcPriFfdJshcqomfe9APxIryRjuKYd6NsDGQuWDHfRma_3DQlSA7sc_RD9qxHJIfHEdhfjKzt4",
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