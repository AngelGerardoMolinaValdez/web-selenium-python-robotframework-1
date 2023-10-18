class DataTableRepository:
    __data_tables: dict = {}

    @classmethod
    def save(cls, object, id):
        cls.__data_tables[id] = object

    @classmethod
    def find(cls, id):
        return cls.__data_tables.get(id)

    @classmethod
    def find_all(cls):
        return cls.__data_tables
