from typing import Generator
from copy import deepcopy


class DictChange:
    record_keys = []

    def __init__(self, dataset: Generator, schema: dict):
        if isinstance(schema, dict):
            self.schema = schema
        else:
            raise ValueError("""
            schema 错误，格式为：schema_example = {"att_source": {'id': '', '2码': "", '3码': ""},
                        'att_natural': {'phonecode': "", 'currency_name': "", 'subregion': ""},
                        'other': {'translations': ""}
                            """)
        self.dataset = dataset
        # self.update_dict()

        # print(type(self.dataset))

    def update_dict(self):
        _dataset = []
        for r in self.dataset:
            res = self._recode_dict_change(r)
            _dataset.append(res)
            #print(_dataset)
        return _dataset

    def _recode_dict_change(self, r):
        return self._schema(r)
        # print(r)

    def _get_r_value(self, r, key):
        """
        根据记录的key查找值
        :param r: 记录
        :param key: 键
        :return: 值
        """
        if key in r:
            return r[key]
        raise ValueError(f'{r}记录中没有找到{key},请检查schema_example中的key是否存在于export_columns中')

    def _value_into_new_schema(self, new_schema, r):
        """
        值装填到新的字典里
        :return: 装填好的结果
        """
        # 判断是否为空树
        if new_schema == {}:
            return {}
        # 递归遍历嵌套字典
        for root_key, root_value in new_schema.items():
            # 是否为叶子节点
            if not isinstance(new_schema[root_key], dict):
                # 更新叶子节点的值
                for root_key in new_schema.keys():
                    if new_schema[root_key] == '':
                        new_schema[root_key] = self._get_r_value(r, root_key)
                return new_schema
            else:
                # 递归非叶子节点
                result = self._value_into_new_schema(new_schema[root_key], r)
                new_schema[root_key] = result
        return new_schema

    def _schema(self, r):
        new_schema: dict = deepcopy(self.schema)
        new_schema = self._value_into_new_schema(new_schema, r)
        return new_schema
