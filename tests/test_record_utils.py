import unittest
import os
from record.record_utils import RecordUtils
from record.record import Record


class TestRecordUtils(unittest.TestCase):

    def setUp(self):
        self.file_path = "test_records.csv"
        with open(self.file_path, "w") as file:
            file.write("id,date,type,category,description,amount\n")

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_add_record(self):
        record = Record("income", "salary", 1000, "Test salary")
        RecordUtils.add_record(record, self.file_path)
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("Test salary", lines[1])

    def test_add_record_invalid_date(self):
        record = Record("income", "salary", 1000, "Test salary")
        record.date = "2024-13-32"
        with self.assertRaises(ValueError):
            RecordUtils.add_record(record, self.file_path)

    def test_add_record_negative_amount(self):
        record = Record("expense", "food", -100, "Test food")
        RecordUtils.add_record(record, self.file_path)
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("-100", lines[1])

    def test_add_record_missing_fields(self):
        with self.assertRaises(TypeError):
            RecordUtils.add_record(Record("income", "salary"), self.file_path)

    def test_add_record_large_amount(self):
        record = Record("income", "salary", 1e10, "Large amount")
        RecordUtils.add_record(record, self.file_path)
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("10000000000.0", lines[1])

    def test_delete_record(self):
        record = Record("income", "salary", 1000, "Test salary")
        RecordUtils.add_record(record, self.file_path)
        RecordUtils.delete_record(record.id, self.file_path)
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 1)

    def test_delete_record_invalid_id(self):
        with self.assertRaises(ValueError):
            RecordUtils.delete_record("invalid-uuid", self.file_path)

    def test_edit_record(self):
        record = Record("income", "salary", 1000, "Test salary")
        RecordUtils.add_record(record, self.file_path)
        updated_record = Record("income", "salary", 2000, "Updated salary")
        RecordUtils.edit_record(record.id, updated_record, self.file_path)
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.assertIn("Updated salary", lines[1])

    def test_edit_record_invalid_id(self):
        updated_record = Record("income", "salary", 2000, "Updated salary")
        with self.assertRaises(ValueError):
            RecordUtils.edit_record("invalid-uuid", updated_record, self.file_path)

    def test_edit_record_negative_amount(self):
        record = Record("income", "salary", 1000, "Test salary")
        RecordUtils.add_record(record, self.file_path)
        updated_record = Record("income", "salary", -2000, "Updated salary")
        RecordUtils.edit_record(record.id, updated_record, self.file_path)
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.assertIn("-2000", lines[1])

    def test_search_records(self):
        record = Record("income", "salary", 1000, "Test salary")
        RecordUtils.add_record(record, self.file_path)
        results = RecordUtils.search_records("salary", self.file_path)
        self.assertEqual(len(results), 1)
        self.assertIn("Test salary", results[0])

    def test_search_records_no_results(self):
        results = RecordUtils.search_records("nonexistent", self.file_path)
        self.assertEqual(len(results), 0)

    def test_calculate_statistics(self):
        record1 = Record("income", "salary", 1000, "Test salary", "2023-06-15")
        record2 = Record("expense", "food", 500, "Test food", "2023-06-16")
        RecordUtils.add_record(record1, self.file_path)
        RecordUtils.add_record(record2, self.file_path)
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        stats = RecordUtils.calculate_statistics(start_date, end_date, self.file_path)
        self.assertEqual(stats["income"], 1000)
        self.assertEqual(stats["expense"], 500)

    def test_calculate_statistics_no_records(self):
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        stats = RecordUtils.calculate_statistics(start_date, end_date, self.file_path)
        self.assertEqual(stats["income"], 0)
        self.assertEqual(stats["expense"], 0)

    def test_calculate_statistics_only_income(self):
        record = Record("income", "salary", 1000, "Test salary", "2023-06-15")
        RecordUtils.add_record(record, self.file_path)
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        stats = RecordUtils.calculate_statistics(start_date, end_date, self.file_path)
        self.assertEqual(stats["income"], 1000)
        self.assertEqual(stats["expense"], 0)

    def test_calculate_statistics_large_date_range(self):
        record = Record("income", "salary", 1000, "Test salary", "2023-06-15")
        RecordUtils.add_record(record, self.file_path)
        start_date = "1900-01-01"
        end_date = "2100-12-31"
        stats = RecordUtils.calculate_statistics(start_date, end_date, self.file_path)
        self.assertEqual(stats["income"], 1000)
        self.assertEqual(stats["expense"], 0)


if __name__ == "__main__":
    unittest.main()
