from .connect import get_es
from conf.conf import AppConfig
from my_log.mylogger import logger

class MyElasticSearch:
    index = AppConfig.elastic_index

    def __init__(self):
        pass

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
            dict.update({source['sliceIndex']:source['content']})

        sorted_dict = sorted(dict.items(), key=lambda x: x[0])
        for key, value in sorted_dict:
            logger.info(f"{key}: {value}")

    def insert_data(self, datas):
        es = get_es()
        es.index(index=self.index, body=datas)

    def query_by_uuid(self,uuid):
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

if __name__ == '__main__':
    pass
    #ElasticSearch().insert_data(None)