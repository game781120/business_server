from elasticsearch import Elasticsearch

# import os
# import sys
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(parent_dir)

from conf import AppConfig
from my_log import logger
# 在模块中定义一个私有变量，用于存储单例对象
_es = None

# 创建索引
mapping = {
    'properties': {
        'uuid': {'type': 'keyword'},
        # 案件类型(案由)
        'caseType': {'type': 'text', 'analyzer': 'ik_smart'},
        # 地点
        'location': {'type': 'text', 'analyzer': 'ik_smart'},
        # 涉案物品
        'article': {'type': 'text', 'analyzer': 'ik_smart'},
        # 案件特殊信息: 自首 酒驾 逃逸
        'special': {'type': 'text', 'analyzer': 'ik_smart'},
        # 伤害情况
        'damage': {'type': 'text', 'analyzer': 'ik_smart'},
        # 案情摘要
        'abstract': {'type': 'text', 'analyzer': 'ik_smart'}
    }
}

def get_es():
    global _es

    # 如果对象已经创建，则直接返回
    if _es is not None:
        # 检查连接是否可用
        try:
            if _es.ping():
                print('Elasticsearch client is connected')
                return _es
            else:
                print('Elasticsearch client is not connected')
        except ConnectionError:
            print('Cannot connect to Elasticsearch')



    url = f'http://{AppConfig.elastic_username}:{AppConfig.elastic_password}@{AppConfig.elastic_host}:{AppConfig.elastic_port}'
    logger.info(f"url={url}")
    _es = Elasticsearch(url)

    #http://10.0.36.13:9200/wenshu_20240329/_mapping
    #curl -XGET http://10.0.36.13:9200/wenshu_20240329/_mapping
    # 检查索引是否存在，如果不存在则创建
    if not _es.indices.exists(index=AppConfig.elastic_index):
        _es.indices.create(index=AppConfig.elastic_index, body={'mappings': mapping})
    else:
        # 获取现有的mapping
        existing_mapping = _es.indices.get_mapping(index=AppConfig.elastic_index)
        existing_properties = existing_mapping[AppConfig.elastic_index]['mappings']['properties']
        # 比较现有的mapping和新的mapping，找出需要删除的字段
        delete_props = []
        for field in existing_properties:
            if field not in mapping['properties']:
                _es.indices.delete_field(index=AppConfig.elastic_index, field=field)
                #delete_props.append(field)

        # 删除字段
        # if delete_props:
        #     body = {"properties": {prop: None for prop in delete_props}}
        #     _es.indices.put_mapping(index=AppConfig.elastic_index, body=body)

        # 添加新的字段

        #_es.indices.put_mapping(index=AppConfig.elastic_index, body=mapping)

        # 检查新字段是否需要添加
        for field in mapping['properties']:
            if field not in existing_properties:
                print(f"---------- field={field}")
                _es.indices.put_mapping(index=AppConfig.elastic_index,
                                        body={'properties': {field: mapping['properties'][field]}})

    return _es


def delete_index():
    url = f'http://{AppConfig.elastic_username}:{AppConfig.elastic_password}@{AppConfig.elastic_host}:{AppConfig.elastic_port}'
    logger.info(f"url={url}")
    _es = Elasticsearch(url)
    # 检查索引是否存在，如果不存在则创建
    if _es.indices.exists(index=AppConfig.elastic_index):
        _es.indices.delete(index=AppConfig.elastic_index)

if __name__ == '__main__':
    #get_es()
    delete_index()