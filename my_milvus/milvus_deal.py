import json
import os
import sys

# 将父目录添加到Python路径中
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from embedding import HttpEmbeddings
from my_milvus.connect import get_collections
from conf import AppConfig
from my_log.mylogger import logger
from pymilvus import Hit

# import random
#
# from pymilvus import DataType, FieldSchema, IndexType, MetricType

# 向数据表中插入一些适量化数据
# num_vectors = 1024
# vectors = [[random.random() for _ in range(512)] for _ in range(num_vectors)]
# data = [{'uuid': str(i), 'data': vector} for i, vector in enumerate(vectors)]
# milvus_client.insert(collection_name=collection_name, records=data)

# 创建索引
# index_param = {"nlist": 512}
# index_type = IndexType.IVF_SQ8
# metric_type = MetricType.L2
# milvus_client.create_index(collection_name, index_type, index_param, metric_type)

# # 进行向量相似度搜索
# query_vector = [random.random() for _ in range(512)]
# top_k = 10
# search_param = {"nprobe": 16}
# search_result = milvus_client.search(collection_name=collection_name, query_records=[query_vector], top_k=top_k, params=search_param)
# print(search_result)


# # 查询与指定向量最相似的向量
# question ="解释一下：湖南移动的数字人"
# #question ="中国人民共和国"
#
# query_vector = HttpEmbeddings().embed_query(question)
# anns_field = 'contentVector'
# search_param = {"metric_type": "L2",
#                 "params": {"nprobe": 16, "nlist": 16384}
#                }
#
# expression = "datasetId == 1772245036587679746 && fileId == 1772245079587684353"
#
# limit = 1
# output_fields: list[str] = ["id", "datasetId", "fileId", "content", "answer"]
#
# # 执行搜索操作
# search_result = client.search(collection_name=collection_name, data=[query_vector], anns_field=anns_field,
#                               param=search_param, limit=limit,
#                               output_fields=output_fields, expression=expression)
# for hit in search_result[0]:
#     if hit:
#         id = hit.id
#         distance = hit.distance
#         score = hit.score
#         # 获取查询结果的实体信息
#         result_entity = hit.entity
#         datasetId = result_entity.get('datasetId')
#         fileId = result_entity.get('fileId')
#         content = result_entity.get('content')
#         answer = result_entity.get('answer')
#         if abs(score) <= 0.16:
#             print(f"score={score}, distance={distance},\n"
#                   f"id={id}, datasetId={datasetId}, fileId={fileId},\n"
#                   f"content={content},\n"
#                   f"answer={answer}")

_METRIC_TYPE = 'L2'
_INDEX_TYPE = 'IVF_FLAT'
_NLIST = 1024
_NPROBE = 16
_TOPK = 6


class MyMilvus:

    def search(self, collection=None, vector_field=None, search_vectors=None, uuid=None):
        search_param = {}
        if uuid:
            query_expr = f'uuid == "{uuid}"'
            return collection.query(query_expr)
        else:
            search_param.update({
                "data": search_vectors,
                "anns_field": vector_field,
                "param": {"metric_type": _METRIC_TYPE, "params": {"nprobe": _NPROBE}},
                "limit": _TOPK
            })

            return collection.search(**search_param)
        # for i, result in enumerate(results):
        #     print("\nSearch result for {}th vector: ".format(i))
        #     for j, res in enumerate(result):
        #         print("Top {}: {}".format(j, res))

    # 插入数据前查询主键是否存在
    def query_by_uuid(self, uuid):

        abstract_collections = get_collections(AppConfig.milvus_collection_abstract)
        result = self.search(collection=abstract_collections, uuid=uuid)

        print(f"query_by_uuid {uuid} result={result}")

        if len(result) == 0:
            return False
        else:
            return True

    def query_data_by_uuid(self, uuid):

        abstract_collections = get_collections(AppConfig.milvus_collection_abstract)

        expression = f'uuid=="{uuid}"'
        search_param = {"metric_type": "L2",
                        "params": {"nprobe": 16, "nlist": 16384}
                        }
        result = abstract_collections.search(data=[], anns_field=None,
                                             param=search_param, limit=1,
                                             output_fields=['uuid'], expression=expression)
        print(f"result={result}")

        for i, item in enumerate(result):
            print(f"location {i + 1}: item={item}")

        # result = article_collections.search(data=[], anns_field=None,
        #                                 param=search_param, limit=1,
        #                                 output_fields=['uuid'], expression=expression)
        # for i, item in enumerate(result):
        #     print(f"article {i + 1}: item={item}")
        #
        #
        # result = damage_collections.search(data=[], anns_field=None,
        #                                param=search_param, limit=1,
        #                                output_fields=['uuid'], expression=expression)
        #
        # for i, item in enumerate(result):
        #     print(f"damage {i + 1}: item={item}")
        #
        #
        #
        # result = abstract_collections.search(data=[], anns_field=None,
        #                                  param=search_param, limit=1,
        #                                  output_fields=['uuid'], expression=expression)
        # for i, item in enumerate(result):
        #     print(f"abstract {i + 1}: item={item}")

    def data_2_str(self, data):
        if isinstance(data, list):
            return ', '.join(data)
        if isinstance(data, dict):
            return json.dumps(data)
        if isinstance(data, str):
            return data

    def delete_data(self, uuid):
        collections = get_collections(AppConfig.milvus_collection_location)
        collections.delete(f'uuid in ["{uuid}"]')

        collections = get_collections(AppConfig.milvus_collection_article)
        collections.delete(f'uuid in ["{uuid}"]')

        collections = get_collections(AppConfig.milvus_collection_damage)
        collections.delete(f'uuid in ["{uuid}"]')

        collections = get_collections(AppConfig.milvus_collection_abstract)
        collections.delete(f'uuid in ["{uuid}"]')

    def flush_collection(self):
        collections = [get_collections(AppConfig.milvus_collection_location),
                       get_collections(AppConfig.milvus_collection_article),
                       get_collections(AppConfig.milvus_collection_damage),
                       get_collections(AppConfig.milvus_collection_abstract)]
        for collection in collections:
            collection.flush()
            print('All records have been flushed')
            # # 获取集合信息
            # info = collection.get_collection_info()
            # total_num, _, _, wal_num = info['row_count'], info['partitions'], info['segments'], info['wal_num']
            # # 检查未落盘的记录数
            # unflushed_num = total_num - wal_num
            # if unflushed_num > 0:
            #     # 落盘操作
            #     collection.flush()
            #     print(f'Flushed {unflushed_num} unflushed records')
            # else:
            #     print('All records have been flushed')

    def insert_data(self, data):
        uuid = data.get("uuid")
        caseType = data.get("caseType")
        location = data.get("location")
        article = data.get("article")
        damage = data.get("damage")
        abstract = data.get("abstract")
        if location:
            print(f"location={location}")
            location = self.data_2_str(location)
            location_vector = HttpEmbeddings().embed_query(location)
            data = [[str(uuid)], [str(caseType)], [location_vector]]
            collections = get_collections(AppConfig.milvus_collection_location)
            collections.insert(data)
        if article:
            print(f"article={article}")
            article = self.data_2_str(article)
            article_vector = HttpEmbeddings().embed_query(article)
            data = [[str(uuid)], [str(caseType)], [article_vector]]
            collections = get_collections(AppConfig.milvus_collection_article)
            collections.insert(data)
        if damage:
            print(f"damage={damage}")
            damage = self.data_2_str(damage)
            damage_vector = HttpEmbeddings().embed_query(damage)
            data = [[str(uuid)], [str(caseType)], [damage_vector]]
            collections = get_collections(AppConfig.milvus_collection_damage)
            collections.insert(data)
        if abstract:
            print(f"abstract={abstract}")
            abstract = self.data_2_str(abstract)
            abstract_vector = HttpEmbeddings().embed_query(abstract)
            data = [[str(uuid)], [str(caseType)], [abstract_vector]]
            collections = get_collections(AppConfig.milvus_collection_abstract)
            collections.insert(data)

    def query_data_by_vector(self, case_type, top=6, article=None, abstract=None, damage=None, uuids=None):

        search_param = {"metric_type": "L2",
                        "params": {"nprobe": 16, "nlist": 16384}
                        }
        expr = f'caseType like "{case_type}%"'
        if uuids:
            expr += f' and uuid in {uuids}'

        anns_field = "abstractVector"  # 默认值
        collection_name = AppConfig.milvus_collection_abstract
        vector = None
        if abstract:
            if type(abstract) == list:
                abstract = ', '.join(abstract)
            vector = HttpEmbeddings().embed_query(abstract)
            collection_name = AppConfig.milvus_collection_abstract
            anns_field = "abstractVector"

        elif article:
            if type(article) == list:
                article = ', '.join(article)
            vector = HttpEmbeddings().embed_query(article)
            collection_name = AppConfig.milvus_collection_article
            anns_field = "articleVector"
        elif damage:
            if type(damage) == list:
                damage = ', '.join(damage)
            vector = HttpEmbeddings().embed_query(damage)
            collection_name = AppConfig.milvus_collection_damage
            anns_field = "damageVector"
        if not vector:
            print(f"vector---------- ={vector}")
            return []
        collections = get_collections(collection_name)
        # print(f"vector ={vector}")
        print(f"collection_name ={collection_name}")
        print(f"anns_field ={anns_field}")
        print(f"collections ={collections}")
        result = collections.search(data=[vector], anns_field=f"{anns_field}",
                                    param=search_param, limit=top,
                                    expr=expr,
                                    output_fields=['uuid'])

        print(f"query_data_by_vector result ={result}")
        data_list = []
        for i, hits in enumerate(result):
            for j, hit in enumerate(hits):
                hit = hit.to_dict()
                distance = hit.get("distance")
                entity = hit.get("entity", None)
                uuid = entity.get("uuid")
                data_list.append({"uuid": uuid, "distance": distance})

        print(f"data_list result ={data_list}")
        return data_list
