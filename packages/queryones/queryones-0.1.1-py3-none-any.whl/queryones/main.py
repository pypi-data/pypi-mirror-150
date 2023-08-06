import sqlite3
from tablevalue import TableValue, Manager
from dictones import DictOnes
import re


def get_field_type(value):
    if type(value) == int:
        return TableValue.Types.INTEGER
    elif type(value) == float:
        return TableValue.Types.REAL
    elif type(value) == str:
        return TableValue.Types.TEXT
    else:
        return TableValue.Types.BLOB


class Query(object):
    def __init__(self, text='', manager=None):
        self.parameters = DictOnes()
        self.text = text
        if manager is None:
            self._conn = sqlite3.connect(':memory:')
            self._manager = Manager(connection=self._conn)
        else:
            self._manager = manager
            self._conn = manager.conn
        self._cur = self._conn.cursor()
        self._last_count_result_tables = 0

    def __check_fill_parameters(self):

        table_params = set(re.findall("into (\w+).*?[\s ]+from (&[а-яА-Яa-zA-Z\d_]+)", self.text))

        tables_for_tmp = list()

        for param in table_params:
            table_name = param[0]
            param_in_text = param[1]
            if self._manager.exists(table_name):
                self._manager.drop_table(table_name)

            if not param_in_text[1:] in self.parameters:
                raise ValueError(f'Parameter [{param_in_text}] not filled in.')
            else:
                table_data = DictOnes()
                table_data.name_param = param_in_text[1:]
                table_data.table_name = table_name
                table_data.table = self.parameters[param_in_text[1:]]

                tables_for_tmp.append(table_data)

        for param in tables_for_tmp:
            new_tmp_table = TableValue(manager=self._manager, table_name=param.table_name)
            for column in param.table.columns:
                new_tmp_table.columns.add(column.name, column.type)
            new_tmp_table.new_bulk_insert(param.table.get_data())
            self.text = self.text.replace(f'&{param.name_param}', param.table_name)
            self.text = self.text.lower().replace(f'into {param.table_name}', '')

        table_params = set(re.findall("from (&[а-яА-Яa-zA-Z\d_]+)", self.text))
        parameters_in_query = set(re.findall("(&[а-яА-Яa-zA-Z\d_]+)", self.text))
        for parameter in parameters_in_query:
            par_name = parameter[1:]
            if not par_name in self.parameters:
                raise ValueError(f'Parameter [{par_name}] not filled in.')
            self.text = self.text.replace(parameter, f':{par_name}')

        return tables_for_tmp

    def execute(self, table_for_result_in_db='ResultTable'):

        tmp_tables = self.__check_fill_parameters()

        # Проверка что тут несколько запросов
        query_to_exec = list()
        all_query = self.text.split(';')
        for query_text in all_query:
            executor = self._cur.execute(query_text, self.parameters)

        pre_result = self._cur.fetchall()
        if len(pre_result):
            one_record = pre_result[0]
        else:
            one_record = None

        self._columns = Query.Column()
        index = 0
        for descr in executor.description:
            if one_record is None:
                type_rec = 'TEXT'
            else:
                type_rec = get_field_type(one_record[index])
            self._columns[descr[0]] = DictOnes('name, type', descr[0], type_rec)
            index += 1

        result = Query.Result(self, table_for_result_in_db + str(self._last_count_result_tables))
        self._last_count_result_tables += 1
        result._table.new_bulk_insert(pre_result)

        for tmp_table in tmp_tables:
            self._manager.drop_table(tmp_table.table_name)

        return result._table

    def execute_pack(self, table_for_result_in_db='ResultTable'):
        tmp_tables = self.__check_fill_parameters()

        # Проверка что тут несколько запросов
        returned_result = list()
        all_query = self.text.split(';')
        for query_text in all_query:
            executor = self._cur.execute(query_text, self.parameters)

            pre_result = self._cur.fetchall()
            if len(pre_result):
                one_record = pre_result[0]
            else:
                one_record = None

            self._columns = Query.Column()
            index = 0
            for descr in executor.description:
                if one_record is None:
                    type_rec = 'TEXT'
                else:
                    type_rec = get_field_type(one_record[index])
                self._columns[descr[0]] = DictOnes('name, type', descr[0], type_rec)
                index += 1

            result = Query.Result(self, table_for_result_in_db + str(self._last_count_result_tables))
            self._last_count_result_tables += 1
            result._table.new_bulk_insert(pre_result)

            returned_result.append(result._table)

        for tmp_table in tmp_tables:
            self._manager.drop_table(tmp_table.table_name)

        return returned_result

    def set_parameter(self, param, value):
        self.parameters[param] = value

    class Column(object):
        def __init__(self):
            self._current = 0

        def __setattr__(self, key, value):
            self.__dict__[key] = value

        def __setitem__(self, key, value):
            self.__dict__[key] = value

        def __iter__(self):
            return self

        def __next__(self):
            index = 0
            for key, value in self.__dict__.items():
                if index-1 == self._current:
                    self._current += 1
                    return value
                index += 1
            raise StopIteration()


    class Result(list):
        # Методы выгрузить(), выбрать(), следующий(), пустой()
        def __init__(self, parent, table_name):
            self._parent = parent
            self._table = TableValue(manager=parent._manager, table_name=table_name)
            for column in self._parent._columns:
                self._table.columns.add(column.name, column.type)

        def count(self):
            return len(self)