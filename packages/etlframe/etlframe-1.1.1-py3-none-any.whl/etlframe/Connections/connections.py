from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from etlframe.Connections.es import EsClient
from etlframe.Connections.sql_connections import SqlaReflectHelper


class DatabaseConnection(object):
    """
    SQL链接类
    """
    db: Engine

    def __init__(self, db):
        if isinstance(db, str):
            self._engine = create_engine(
                db,
                max_overflow=10,  # 超过连接池大小外最多创建的连接
                pool_size=50,  # 连接池大小
                pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
                pool_recycle=3600,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                echo=False)
        else:
            raise ValueError("db 参数类型错误")

    @property
    def db(self) -> SqlaReflectHelper:
        return SqlaReflectHelper(self._engine)


class ElasticsearchConnection(object):
    """
    es 链接类
    """
    _client = None

    def __init__(self, es_params=None):
        if es_params is None:
            es_params = {}
        self.es_params = es_params

    @property
    def client(self):
        if self._client is None:
            self._client = EsClient(**self.es_params)
        return self._client
