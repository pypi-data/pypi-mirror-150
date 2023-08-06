import itertools

import nb_log
from pymysql.cursors import Cursor
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, CursorResult
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker, DeclarativeMeta
from sqlalchemy.orm.scoping import ScopedSession
# sqlachemy的日志还是非最终完全sql语句，这里可以显示完全最终语句。
from sqlalchemy.util import Properties

from etlframe.Decorator.decorator import flyweight
from etlframe.Mapping.heapler import get_records

logger_show_pymysql_execute_sql = nb_log.LogManager('show_pymysql_execute_sql').get_logger_and_add_handlers(
    log_filename='show_pymysql_execute_sql.log')


def _my_mogrify(self, query, args=None):
    """
    Returns the exact string that is sent to the database by calling the
    execute() method.
    This method follows the extension to the DB API 2.0 followed by Psycopg.
    """
    conn = self._get_db()
    if args is not None:
        query = query % self._escape_args(args, conn)
    # logger_show_pymysql_execute_sql.debug(query)
    return query


Cursor.mogrify = _my_mogrify


class _SessionContext(Session):
    """
    自动关闭
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()
        return False


class Table:
    """
    表类
    """

    def __init__(self, sql_session: Session, base_classes: Properties, table_name: str):
        self._session = sql_session
        self.table_name = table_name
        self.table_name_obj = getattr(base_classes, table_name)

    def get_columns(self) -> list:
        """
        列名
        :return:
        """
        return self.table_name_obj.__table__.columns.keys()


class Records(object):
    """
    查询到的结果类
    """

    def __init__(self, rows):
        self._rows = rows
        self._limit_num = None

    def __iter__(self):
        return self

    def next(self):
        return next(self._rows)

    __next__ = next

    def map(self, function):
        self._rows = (function(r) for r in self._rows)
        return self

    def filter(self, function):
        self._rows = (r for r in self._rows if function(r))
        return self

    def rename(self, mapper):
        """
        字段重命名
        """

        def function(record):
            if isinstance(record, dict):
                return {mapper.get(k, k): v for k, v in record.items()}
            else:
                return dict(zip(mapper, record))

        return self.map(function)

    def limit(self, num):
        def rows_limited(rows, limit):
            for i, r in enumerate(rows):
                if i < limit:
                    yield r
                else:
                    return None

        self._rows = rows_limited(self._rows, num)
        return self

    def get_one(self):
        r = self.get(1)
        return r[0] if len(r) > 0 else None

    def get(self, num):
        return [i for i in itertools.islice(self._rows, num)]

    def get_all(self):
        return [r for r in self._rows]

    # def to_df(self, batch_size=None):
    #     if batch_size is None:
    #         import pandas
    #         return pandas.DataFrame.from_records(self)
    #     else:
    #         return to_df_iterator(self, batch_size)

    # def to_csv(self, file_path, sep=',', header=False, columns=None, batch_size=100000, **kwargs):
    #     """
    #     用于大数据量分批写入文件
    #     :param file_path: 文件路径
    #     :param sep: 分割符号，hive默认\001
    #     :param header: 是否写入表头
    #     :param columns: 按给定字段排序
    #     :param batch_size: 每批次写入文件行数
    #     """
    #     mode = "w"
    #     for df in self.to_df(batch_size=batch_size):
    #         df.to_csv(file_path, sep=sep, index=False, header=header, columns=columns, mode=mode, **kwargs)
    #         mode = "a"
    #         header = False


@flyweight
class SqlaReflectHelper(nb_log.LoggerMixin):
    """
    反射数据库中已存在的表
    """
    table: DeclarativeMeta

    def __init__(self, sqla_engine: Engine):
        nb_log.LogManager('sqlalchemy.engine.base.Engine').remove_all_handlers()
        if sqla_engine.echo:
            # 将日志自动记录到硬盘根目录的/pythonlogs/sqla_execute.log。原来的日志模板不好看，换成这个。
            nb_log.LogManager('sqlalchemy.engine.base.Engine').get_logger_and_add_handlers(10,
                                                                                           log_filename='sqla_execute.log')
        else:
            nb_log.LogManager('sqlalchemy.engine.base.Engine').get_logger_and_add_handlers(30,
                                                                                           log_filename='sqla_execute.log')
        self.engine = sqla_engine
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        self.base_classes = Base.classes
        self.base_classes_keys = Base.classes.keys()
        # self.logger.debug(self.base_classes_keys)
        # self.show_tables_and_columns()
        self.session_factory_of_scoped = None

    # def show_tables_and_columns(self):
    #     """
    #     获取所有的表和列名
    #     :return:
    #     """
    #     for table_name in self.base_classes_keys:
    #         self.logger.debug(table_name)
    #         model = getattr(self.base_classes, table_name)
    #         self.logger.debug(model.__table__.columns.keys())

    def get_session_factory(self):
        """
        session工厂
        :return:
        """
        return sessionmaker(bind=self.engine)

    def get_session_factory_of_scoped(self) -> ScopedSession:
        """
        可以修改session为打开自动关闭
        :return:
        """
        session_factory = sessionmaker(bind=self.engine)  # 改成了自定义的Session类 , class_=_SessionContext
        return ScopedSession(session_factory)

    @property
    def session(self) -> Session:
        """

        :return:
        """
        if not self.session_factory_of_scoped:
            self.session_factory_of_scoped = self.get_session_factory_of_scoped()
        return self.session_factory_of_scoped()

    def get_table(self, table_name) -> Table:
        return Table(self.session, self.base_classes, table_name)

    def get_columns(self) -> list:
        # print(self.__dict__)
        return self.table.__table__.columns.keys()

    # def read(self, text, batch_size):
    #     res = self.session.execute(text)
    #
    #     # for res.fetchmany(batch_size))

    def read(self, sql, args=None, batch_size=10000, columns=None):
        """
        查询返回所有表记录
        :param sql: sql语句
        :param args: sql语句参数
        :param batch_size: 每次查询返回的缓存的数量，大数据量可以适当提高大小
        :return: 生成器对象
        """
        r: CursorResult = self.session.execute(sql, args)
        records = get_records(r, batch_size, columns)
        return Records(records)


if __name__ == '__main__':
    """
    例如 ihome_area2的表结果如下。

    create table ihome_area2
(
    create_time datetime    null,
    update_time datetime    null,
    id          int auto_increment
        primary key,
    name        varchar(32) not null
);
    """

    enginex = create_engine(
        'mysql+pymysql://root:nOGgLx6fDQ2tQDx1@127.0.0.1:3306/country?charset=utf8mb4',
        max_overflow=10,  # 超过连接池大小外最多创建的连接
        pool_size=50,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=3600,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
        echo=False)
    db = SqlaReflectHelper(enginex)
    session = db.session
    print(dir(session.query))
    # print(db.get_table('countries').get_columns())

    text = 'select id, name, iso3 from  countries where 1=1'
    batch_size = 10
    db.read(text, batch_size)
    # table = sqla_helper.get_table('countries')
    # # print(type(table))
    # all = sqla_helper.query(table).all()
    # print(all)
    # print(sqla_helper)
    # Ihome_area2 = sqla_helper.base_classes.ihome_area2  # ihome_area2是表名。

    # def f1():
    #     with sqla_helper.session as ss:
    #         ss  # type: _SessionContext
    #
    #         print(ss)

    # print(ss.query(sqlalchemy.func.count(Ihome_area2.id)).scalar())
    #
    #         # 使用orm方式插入
    #         ss.add(Ihome_area2(create_time=datetime.now(), update_time=datetime.now(), name='testname'))
    #
    #         print(ss.query(sqlalchemy.func.count(Ihome_area2.id)).scalar())
    #
    #         # 使用占位符语法插入，此种可以防止sql注入
    #         ss.execute(f'''INSERT INTO ihome_area2 (create_time, update_time, name) VALUES (:v1,:v2,:v3)''',
    #                    params={'v1': '2020-06-14 19:15:14', 'v2': '2020-06-14 19:15:14', 'v3': 'testname00'})
    #
    #         # 直接自己拼接完整字符串，不使用三方包占位符的后面的参数，此种会引起sql注入，不推荐。
    #         cur = ss.execute(
    #             f'''INSERT INTO ihome_area2 (create_time, update_time, name) VALUES ('2020-06-14 19:15:14','2020-06-14 19:15:14', 'testname')''', )
    #
    #         # 这样也可以打印执行的语句
    #         # noinspection PyProtectedMember
    #         print(cur._saved_cursor._executed)
    #
    #     # 使用最原生的语句，直接调用了pymysql的cursor对象。
    #     conny = sqla_helper.engine.raw_connection()
    #     cury = conny.cursor(DictCursor)  # type: DictCursor
    #     print(cury)
    #     cury.execute('SELECT * FROM ihome_area2 LIMIT 3')
    #     result = cury.fetchall()
    #     print(result)
    #     conny.commit()
    #     cury.close()
    #     conny.close()
    #
    #
    # def f2():
    #     ss = sqla_helper.get_session_factory()()
    #     print(ss)
    #     print(ss.query(sqlalchemy.func.count(sqla_helper.base_classes.ihome_area.id)).scalar())
    #     ss.add(sqla_helper.base_classes.ihome_area(create_time=datetime.now(), update_time=datetime.now(),
    #                                                name='testname'))
    #     ss.commit()
    #     print(ss.query(sqlalchemy.func.count(sqla_helper.base_classes.ihome_area.id)).scalar())
    #     ss.close()
