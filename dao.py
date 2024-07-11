# -*- coding: utf-8 -*-

import pymongo
import os
import logging
import json

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongo_host = "localhost"  # 修改为你的 MongoDB 主机
mongo_port = 27017        # 修改为你的 MongoDB 端口

class database(object):
    def __init__(self, prefix):
        logger.info(f"connect to mongodb {mongo_host}:{mongo_port}")

        # 连接到mongodb
        self.client = pymongo.MongoClient(mongo_host, mongo_port)

        # 创建数据库
        db_name = os.getenv("DB_NAME", "info")

        self.db = self.client[db_name]
        self.collection_path = "user_info"

        logger.info(f"MongoDB initialized: {db_name}/{self.collection_path}")

        self.collection = self.db[self.collection_path]

    def insert_user_data(self, user_id: str, data: list) -> None:
        self.collection.update_one({'user_id': user_id}, {'$set': {'data': data}}, upsert=True)

    def if_exist(self, user_id: str) -> bool:
        result = self.collection.find_one({"user_id": user_id})
        return result is not None

    def export_and_del(self, export_path: str):
        cursor = self.collection.find({})
        documents = {doc['user_id']: doc['data'] for doc in cursor}
        with open(export_path, "w", encoding="utf-8") as file:
            json.dump(documents, file, default=str, ensure_ascii=False, indent=4)
        logger.info(f"Collection {self.collection_path} has been exported to {export_path}")
        self.collection.drop()
        del self.collection
        logger.info(f"Collection {self.collection_path} has been deleted")
        self.client.close()
