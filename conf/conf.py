import yaml
import os
from my_log import logger

class Config:
    # base path
    AppConfDirPath = os.path.dirname(os.path.normpath(os.path.realpath(__file__)))
    logger.info(f"AppConfDirPath={AppConfDirPath}")
    AppRootPath = os.path.dirname(AppConfDirPath)
    logger.info(f"AppRootPath={AppRootPath}")
    AppStaticPath = os.path.join(AppRootPath, "static")
    logger.info(f"AppStaticPath={AppStaticPath}")

    def __init__(self):
        logger.info(f"Config __init__")
        self.is_debug = True
        self.path = os.path.join(self.AppStaticPath)
        logger.info(f"path ={self.path}")
        self.__conf = self.__load_env(f'{self.path}/conf.yml')

    @staticmethod
    def __load_env(env_file_name):
        file = open(os.path.join(os.path.dirname(__file__), env_file_name), 'r', encoding='utf-8')
        yml = yaml.safe_load(file)
        return yml

    @property
    def elastic_config(self):
        return self.__conf.get('elastic', None) if self.__conf else None

    @property
    def elastic_host(self):
        return self.elastic_config.get('host', "127.0.0.1") if self.elastic_config else "127.0.0.1"

    @property
    def elastic_port(self):
        return self.elastic_config.get('port', 19200) if self.elastic_config else 19200

    @property
    def elastic_username(self):
        return self.elastic_config.get('username', "elastic") if self.elastic_config else "elastic"

    @property
    def elastic_password(self):
        return self.elastic_config.get('password', "U6xT2NkcEQ10a") if self.elastic_config else "U6xT2NkcEQ10a"

    @property
    def elastic_knn_boost(self):
        return self.elastic_config.get('knn_boost', 0.1) if self.elastic_config else 0.1

    @property
    def elastic_index(self):
        return self.elastic_config.get('index', "segments") if self.elastic_config else "segments"

    @property
    def embeddings(self):
        return self.__conf['embeddings']

    @property
    def embedding_server(self):
        return self.embeddings['embedding_server']

    @property
    def embedding_name(self):
        return self.embeddings['embedding_name']

    @property
    def mysql_config(self):
        return self.__conf.get('mysql', {})

    @property
    def mysql_host(self):
        return self.mysql_config.get('mysqlHost')

    @property
    def mysql_port(self):
        return self.mysql_config.get('mysqlPort')

    @property
    def db_name_001(self):
        return self.mysql_config.get('db_name_001')

    @property
    def mysql_username(self):
        return self.mysql_config.get('mysqlUser')

    @property
    def mysql_user_password(self):
        return self.mysql_config.get('mysqlPwd')


    @property
    def milvus(self):
        return self.__conf['milvus']

    @property
    def milvus_host(self):
        return self.milvus['host']

    @property
    def milvus_port(self):
        return self.milvus['port']

    @property
    def milvus_db_name(self):
        return self.milvus['dbName']

    @property
    def milvus_collection_location(self):
        return self.milvus['collection_location']

    @property
    def milvus_collection_article(self):
        return self.milvus['collection_article']

    @property
    def milvus_collection_damage(self):
        return self.milvus['collection_damage']

    @property
    def milvus_collection_abstract(self):
        return self.milvus['collection_abstract']




    @property
    def milvus_user(self):
        return self.milvus['user']

    @property
    def milvus_password(self):
        return self.milvus['password']

AppConfig = Config()
