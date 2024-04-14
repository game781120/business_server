import time

from my_log.mylogger import logger
from conf.conf import AppConfig
# from elastic.search import ElasticSearch
from business.caipan_wenshu import (query_data,
                                    xlsx_file_to_table,


                                    data_cleaning_first,
                                    data_to_es_milvus_mysql
                                    )
from my_milvus import create_milvus_connections

from utils import xlsx_file_parsing as xlsx_parsing
from utils import xlsx_file_append as xlsx_append

import os

from flask import Flask, request, jsonify
# import task

app = Flask(__name__)

import sys

parent_path = os.path.dirname(os.path.abspath(__file__))
# packet_path = [
#     os.path.join(parent_path, "my_log"),
#     os.path.join(parent_path, "conf"),
#     os.path.join(parent_path, "my_milvus"),
#     os.path.join(parent_path, "my_elastic"),
#     os.path.join(parent_path, "my_mysql")
#     ]
# print(f"packet_path={packet_path}")
# sys.path.extend(packet_path)

model_api_key = "RBbNKRkaNaOu78agDa03055224864b88A071067fA99177Fb"
model_api_base = "https://brain.thundersoft.com/brain"
# model_ok = "rubik-law-chat"
model_ok = "rubik-chat"


# model_ok = "azure-gpt-3.5-turbo-16k"
@app.route('/chat', methods=['POST'])
def handle_post_request():
    # 假设客户端发送JSON数据，使用request.json获取数据
    data = request.json
    question = data.get("question", None)
    api_base = data.get("api_base", None)
    api_key = data.get("api_key", None)
    model = data.get("model", None)

    print(f"handle_post_request model={model}")
    print(f"handle_post_request model={question}")

    if not question or not model or not api_key or not api_base:
        return jsonify(data), 200

    res = query_data(content=question, is_stream=False, model=model,
                     top=10, token=api_key, url=api_base)

    return jsonify(res), 200


if __name__ == '__main__':
    logger.info("main入口进入")
    logger.info(f"elastic_host = {AppConfig.elastic_host}")
    logger.info(f"elastic_port = {AppConfig.elastic_port}")
    logger.info(f"elastic_username = {AppConfig.elastic_username}")
    logger.info(f"elastic_password = {AppConfig.elastic_password}")
    logger.info(f"elastic_index = {AppConfig.elastic_index}")
    logger.info(f"elastic_knn_boost = {AppConfig.elastic_knn_boost}")
    create_milvus_connections()
    #query_wenshu_case_type()

    # --------------------------
    # file_name = "/home/ubuntu/yjq/poc_business_server/business/caipan_wenshu/files/source_files/2012年09月裁判文书数据.xlsx"
    # xlsx_file_to_table(file_name,"Sheet1", 100, True)


    # --------------------------
    #file_name01 = "/home/ubuntu/yjq/poc_business_server/business/caipan_wenshu/files/source_files/test001.xlsx"
    #data = [["数据001","000","1111"],["数据002","200","2111"],["数据003","300","3111"]]
    #xlsx_append(file_name01,"测试啊",data)

    # --------------------------
    #data_cleaning_first("纠纷")

    # --------------------------
    # file_name = "/home/ubuntu/yjq/poc_business_server/business/caipan_wenshu/files/source_files/2012年08月裁判文书数据.xlsx"
    # for data in xlsx_parsing(file_name, 2, "Sheet1"):
    #     print(data)
    #     time.sleep(30)

    # --------------------------
    # data_to_es_milvus_mysql()

    # --------------------------
    app.run(debug=False, host="0.0.0.0", port=7733)
