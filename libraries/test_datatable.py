import os
import unittest
from datatable import DataTable
from datatable_repository import DataTableRepository

BASE_DIR: str = os.path.dirname(__file__)
TEST_DATA_PATH: str = os.path.join(BASE_DIR, "test_data.csv")
TEST_DATA2_PATH: str = os.path.join(BASE_DIR, "test_data2.csv")

class TestDataTable(unittest.TestCase):
    def test_create(self):
        data_class, id_data_class = DataTable.create(TEST_DATA_PATH, 0)
        self.assertEqual(data_class.tipo_de_cuenta, 'CHECKING')
        self.assertEqual(data_class.cuenta_de_referencia, '13344')
        self.assertEqual(id_data_class, 0)

        data_class, id_data_class = DataTable.create(TEST_DATA_PATH, 1)
        self.assertEqual(data_class.tipo_de_cuenta, 'SAVING')
        self.assertEqual(data_class.cuenta_de_referencia, '13344')
        self.assertEqual(id_data_class, 1)

    def test_multi_create(self):
        data_class, id_data_class = DataTable.create(TEST_DATA_PATH, 0)
        self.assertEqual(data_class.tipo_de_cuenta, 'CHECKING')
        self.assertEqual(id_data_class, 0)

        data_class, id_data_class = DataTable.create(TEST_DATA2_PATH, 0)
        self.assertEqual(data_class.another_field, 'true')
        self.assertEqual(id_data_class, 0)

    def test_save(self):
        data_class, id_data_class = DataTable.create(TEST_DATA_PATH, 0)
        DataTable.save(data_class, id_data_class)
        saved_data_class = DataTableRepository.find(id_data_class)
        self.assertEqual(saved_data_class, data_class)

        another_data_class, another_id_data_class = DataTable.create(TEST_DATA_PATH, 1)
        DataTable.save(another_data_class, another_id_data_class)
        another_saved_data_class = DataTableRepository.find(another_id_data_class)
        self.assertEqual(another_saved_data_class, another_data_class)


class TestDataTableRepository(unittest.TestCase):
    def test_save_and_find(self):
        data_class, id_data_class = DataTable.create(TEST_DATA_PATH, 0)
        DataTableRepository.save(data_class, id_data_class)
        found_data_class = DataTableRepository.find(id_data_class)
        self.assertEqual(found_data_class, data_class)

        another_data_class, another_id_data_class = DataTable.create(TEST_DATA_PATH, 1)
        DataTableRepository.save(another_data_class, another_id_data_class)
        another_found_data_class = DataTableRepository.find(another_id_data_class)
        self.assertEqual(another_found_data_class, another_data_class)

    def test_find_all(self):
        all_data_classes = DataTableRepository.find_all()
        self.assertIsInstance(all_data_classes, dict)