import json

# from pymilvus import connections
from pymilvus import Milvus, connections, db, Collection, CollectionSchema, FieldSchema, DataType, utility
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from conf import AppConfig


def get_collections(name):
    try:
        collection = Collection(name=name)
        return collection
    except Exception as e:
        print(f"Error: {e}")
        print("Trying to reconnect Milvus...")
        # 重新连接Milvus
        create_milvus_connections()
        # 再次创建Collection
        collection = Collection(name=name)
        return collection

def create_milvus_connections():
    connections.connect(host=AppConfig.milvus_host, port=AppConfig.milvus_port)
    if AppConfig.milvus_db_name not in db.list_database():
        db.create_database(AppConfig.milvus_db_name)
        connections.disconnect("default")

    connections.connect(host=AppConfig.milvus_host, port=AppConfig.milvus_port,db_name = AppConfig.milvus_db_name)

    field1 = FieldSchema(name="uuid", dtype=DataType.VARCHAR, description="string",
                             max_length=128, is_primary=True)
    field2 = FieldSchema(name="caseType", dtype=DataType.VARCHAR, description="string",
                             max_length=128, is_primary=False)

    if not utility.has_collection(AppConfig.milvus_collection_location):
        field3 = FieldSchema(name="locationVector", dtype=DataType.FLOAT_VECTOR, description="float vector", dim=1024,
                         is_primary=False)

        schema = CollectionSchema(fields=[field1, field2, field3], description="location collection")
        collection = Collection(name=AppConfig.milvus_collection_location, schema=schema)
        index_param = {
            "index_type": 'IVF_FLAT',
            "params": {"nlist": 1024},
            "metric_type": 'L2'}
        collection.create_index("locationVector", index_param)
        collection.load()

    if not utility.has_collection(AppConfig.milvus_collection_article):
        field3 = FieldSchema(name="articleVector", dtype=DataType.FLOAT_VECTOR, description="float vector", dim=1024,
                         is_primary=False)

        schema = CollectionSchema(fields=[field1, field2, field3], description="article collection")
        collection = Collection(name=AppConfig.milvus_collection_article, schema=schema)
        index_param = {
            "index_type": 'IVF_FLAT',
            "params": {"nlist": 1024},
            "metric_type": 'L2'}
        collection.create_index("articleVector", index_param)
        collection.load()

    if not utility.has_collection(AppConfig.milvus_collection_damage):
        field3 = FieldSchema(name="damageVector", dtype=DataType.FLOAT_VECTOR, description="float vector", dim=1024,
                         is_primary=False)

        schema = CollectionSchema(fields=[field1, field2, field3], description="damage collection")
        collection = Collection(name=AppConfig.milvus_collection_damage, schema=schema)
        index_param = {
            "index_type": 'IVF_FLAT',
            "params": {"nlist": 1024},
            "metric_type": 'L2'}
        collection.create_index("damageVector", index_param)
        collection.load()

    if not utility.has_collection(AppConfig.milvus_collection_abstract):
        field3 = FieldSchema(name="abstractVector", dtype=DataType.FLOAT_VECTOR, description="float vector", dim=1024,
                         is_primary=False)

        schema = CollectionSchema(fields=[field1, field2, field3], description="abstract collection")
        collection = Collection(name=AppConfig.milvus_collection_abstract, schema=schema)
        index_param = {
            "index_type": 'IVF_FLAT',
            "params": {"nlist": 1024},
            "metric_type": 'L2'}
        collection.create_index("abstractVector", index_param)
        collection.load()




def delete_collections():
    connections.connect(host=AppConfig.milvus_host, port=AppConfig.milvus_port, db_name=AppConfig.milvus_db_name)
    collection = Collection(name=AppConfig.milvus_collection_location)
    if collection:
        collection.drop()
    collection = Collection(name=AppConfig.milvus_collection_article)
    if collection:
        collection.drop()
    collection = Collection(name=AppConfig.milvus_collection_damage)
    if collection:
        collection.drop()
    collection = Collection(name=AppConfig.milvus_collection_abstract)
    if collection:
        collection.drop()

    connections.disconnect()





if __name__ == '__main__':
    #delete_collections()
    create_milvus_connections()
    #pass
