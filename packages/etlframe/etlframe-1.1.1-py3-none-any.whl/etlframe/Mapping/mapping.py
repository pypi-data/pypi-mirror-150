
# class ColumnsMapping(object):
#
#     def __init__(self, columns, is_all_columns):
#         """
#
#         :param columns: 所有的列名
#         :param all_results: 是否需要所有的列名
#         """
#         self.raw_columns = columns
#         # self.is_all_columns = is_all_columns
#         self.alias, self.columns = self.get_src_columns_alias()
#
#     def get_src_columns_alias(self):
#         alias = {}

        # if self.is_all_columns:
        #     alias = {}
        #     for k, v in self.raw_columns.items():
        #         pass
        #         if isinstance(v, (list, tuple)):
        #             for i, name in enumerate(v):
        #                 alias.setdefault(name, "%s_%s" % (k, i))
        #         else:
        #             # alias.setdefault(v, k)
        #             alias[v] = k
        #     columns = {}
        #     for k, v in self.raw_columns.items():
        #         if isinstance(v, (list, tuple)):
        #             columns[k] = tuple(alias[n] for n in v)
        #         else:
        #             columns[k] = alias[v]
        #     return alias, columns
        # else:
        #     alias = {}
        #     for k, v in self.raw_columns.items():
        #         if isinstance(v, (list, tuple)):
        #             for i, name in enumerate(v):
        #                 alias.setdefault(name, "%s_%s" % (k, i))
        #         else:
        #             alias.setdefault(v, k)
        #     columns = {}
        #     for k, v in self.raw_columns.items():
        #         if isinstance(v, (list, tuple)):
        #             columns[k] = tuple(alias[n] for n in v)
        #         else:
        #             columns[k] = alias[v]
        #     return alias, columns


class Mapping(object):

    def __init__(self, columns, functions, apply_function):
        self.columns = columns
        self.functions = functions
        self.apply_function = apply_function
        self.total = 0

    def __call__(self, record):
        result = {}
        for k, v in self.columns.items():
            if isinstance(v, (list, tuple)):
                result[k] = self.functions.get(k, lambda x: ",".join(map(str, x)))(
                    tuple(record.get(n) for n in v))
            else:
                value = record.get(v)
                # print(value)
                result[v] = self.functions[k](value) if k in self.functions else value
        # print(result)
        self.total += 1
        return self.apply_function(result)
