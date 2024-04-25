class DataTableIterator:
    def __init__(self, data_table):
        self.__data_table = data_table
        self.__row_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__row_index < len(self.__data_table):
            row = self.__data_table[self.__row_index]
            self.__row_index += 1
            return row
        else:
            raise StopIteration

class DataTableCollection:
    def __init__(self):
        self.__data_tables = []

    def add_data_table(self, data_table):
        self.__data_tables.append(data_table)
    
    def add_data_tables(self, *data_tables):
        for data_table in data_tables:
            self.add_data_table(data_table)

    def create_iterator(self):
        return DataTableIterator(self.__data_tables)