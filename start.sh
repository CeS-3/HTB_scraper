#!/bin/bash

# 检查pymongo库是否安装
if python3 -c "import pymongo" &> /dev/null
then
    echo "pymongo库已安装。"
else
    echo "pymongo库未安装。安装pymongo库..."
    pip install pymongo
    if [ $? -ne 0 ]; then
        echo "pymongo库安装失败。"
        exit 1
    fi
    echo "pymongo库安装成功。"
fi

# 检查Docker是否已安装
if ! command -v docker &> /dev/null
then
    echo "Docker未安装。请先安装Docker。"
    exit
fi

echo "Docker已安装。"

# 拉取MongoDB镜像
echo "拉取MongoDB镜像..."
docker pull mongo

# 检查镜像是否拉取成功
if [ $? -ne 0 ]; then
    echo "MongoDB镜像拉取失败。"
    exit 1
fi

echo "MongoDB镜像拉取成功。"

# 运行MongoDB容器
echo "运行MongoDB容器..."

#创建挂载目录
mkdir volumn_user_info_data

#运行容器
docker run -d --name mongodb -p 27017:27017 -v ./volumn_user_info_data:/data/db mongo

# 检查容器是否运行成功
if [ $? -ne 0 ]; then
    echo "MongoDB容器运行失败。"
    exit 1
fi

echo "MongoDB容器运行成功。"

# 检查容器是否正在运行
docker ps | grep mongodb

if [ $? -ne 0 ]; then
    echo "MongoDB容器未能成功启动。"
    exit 1
fi

echo "MongoDB容器正在运行。"

python3 user_info_scraper.py