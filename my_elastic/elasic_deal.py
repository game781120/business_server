import json

import requests

from my_elastic.connect import get_es
from conf import AppConfig
from my_log import logger

#import nltk


class MyElasticSearch:
    index = AppConfig.elastic_index
    # nltk.download('punkt')
    # nltk.download('averaged_perceptron_tagger')

    def __init__(self):
        pass

    def pre_analyzer(self, analyzer_content):
        # 定义 Elasticsearch 服务器的 URL
        url = f'http://{AppConfig.elastic_host}:{AppConfig.elastic_port}/_analyze'
        payload = {
            'analyzer': 'ik_smart',
            'text': analyzer_content
        }
        response = requests.post(url, json=payload)
        data = response.json()
        if "tokens" in data:
            return [token['token'] for token in data['tokens']]
        else:
            return []

    # def getNoun(self, data):
    #     tokens = nltk.word_tokenize(data)
    #     tags = nltk.pos_tag(tokens)
    #     for word, pos in tags:
    #         print(f"word={word} pos={pos}")
    #
    #     nouns = [word for word, pos in tags if pos in ['NN', 'NNS', 'NNP', 'NNPS']]
    #     print("----------------------")
    #     print(nouns)
    #     return nouns

    def data_2_str(self, data):
        if isinstance(data, list):
            return ', '.join(data)
        if isinstance(data, dict):
            return json.dumps(data)
        if isinstance(data, str):
            return data

    def search_by_datasetId_head1(self, datasetId, head1=""):
        if not datasetId or not head1:
            return None

        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"datasetId": datasetId}},
                    ]
                }
            }
        }

        logger.info(f"es index {self.index} query={query}")
        res = get_es().search(index=self.index, body=query)
        dict = {}
        hits = res['hits']['hits']
        for hit in hits:
            source = hit['_source']
            dict.update({source['sliceIndex']: source['content']})

        sorted_dict = sorted(dict.items(), key=lambda x: x[0])
        for key, value in sorted_dict:
            logger.info(f"{key}: {value}")

    def insert_data(self, uuid, data):
        location = data.get("location")
        article = data.get("article")
        damage = data.get("damage")
        if location:
            if not isinstance(location, str):
                location = self.data_2_str(location)
            data["location"] = location
        if article:
            if not isinstance(article, str):
                article = self.data_2_str(article)
            data["article"] = article
        if damage:
            if not isinstance(damage, str):
                damage = self.data_2_str(damage)
            data["damage"] = damage

        es = get_es()
        es.index(index=self.index, id=uuid, body=data)

    def update_data(self, uuid, data):
        es = get_es()
        # 发送更新请求
        es.update(index=AppConfig.elastic_index,
                  id=uuid,
                  body={"doc": data})

    def query_by_uuid(self, uuid):
        es = get_es()
        # 设置查询条件
        query = {
            'query': {
                'term': {
                    'uuid': {
                        'value': f'{uuid}'
                    }
                }
            }
        }
        # 查询文档
        result = es.search(index=self.index, body=query)
        # 处理查询结果
        for hit in result['hits']['hits']:
            print(hit['_source'])
            return True
        return False

    def query_by_analyzer(self, case_type, article):
        es = get_es()
        query = {
            "query": {
                "bool": {
                    "must": [{"term": {"caseType": case_type}}, ],
                    "should": [
                        {
                            "multi_match": {
                                "query": article,
                                "fields": ['article^1.0'],  # 定义多个字段的权重
                            }
                        },
                    ],
                }
            }
        }
        # 查询文档
        result = es.search(index=self.index, body=query)
        # 处理查询结果
        uuids = []
        for hit in result['hits']['hits']:
            data = hit['_source']
            uuids.append(data.get("uuid"))

        return uuids


if __name__ == '__main__':
    pass
    # ElasticSearch().insert_data(None)
