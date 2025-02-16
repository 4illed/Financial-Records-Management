import csv
import datetime

from record.record import Record


class RecordUtils:
    """
    Класс для работы с финансовыми записями.
    """

    @staticmethod
    def add_record(record: Record, file_path):
        """
        Добавляет новую запись в файл.

        :param record: Объект Record, представляющий новую запись.
        :param file_path: Путь к файлу для сохранения записи.
        """
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(
                file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(record.to_list())

    @staticmethod
    def delete_record(uuid, file_path):
        """
        Удаляет запись по UUID.
        """
        try:
            with open(file_path, "r") as file:
                lines = list(csv.reader(file))

            # Ищем запись по UUID
            updated_lines = []
            found = False
            for line in lines:
                if line[0] == uuid:
                    found = True
                else:
                    updated_lines.append(line)

            if not found:
                print(f"Ошибка: Запись с UUID {uuid} не найдена.")
                return False

            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_lines)
            return True

        except Exception as e:
            print(f"Ошибка при удалении: {e}")
            return False

    @staticmethod
    def edit_record(record_id, updated_record: Record, file_path):
        """
        Обновляет запись по ID.

        :param file_path: Путь к файлу с записями.
        :param record_id: ID записи для обновления.
        :param updated_record: Объект Record с обновленными данными.
        """
        with open(file_path, "r") as file:
            lines = list(csv.reader(file))

        if 0 < record_id <= len(lines):
            lines[record_id] = updated_record.to_list()

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lines)

    @staticmethod
    def search_records(search_term, file_path):
        """
        Ищет записи по категории.

        :param file_path: Путь к файлу с записями.
        :param search_term: Категория для поиска.
        :return: Список найденных записей.
        """
        results = []
        with open(file_path, "r") as file:
            lines = csv.reader(file)
            next(lines)  # Пропускаем заголовок
            for parts in lines:
                if search_term.lower() in parts[2].lower():
                    results.append(parts)
        return results

    @staticmethod
    def calculate_statistics(start_date, end_date, file_path):
        """
        Рассчитывает статистику доходов и расходов за указанный период.

        :param file_path: Путь к файлу с записями.
        :param start_date: Начальная дата периода.
        :param end_date: Конечная дата периода.
        :return: Словарь с суммами доходов и расходов.
        """
        stats = {"income": 0, "expense": 0}
        with open(file_path, "r") as file:
            lines = csv.reader(file)
            next(lines)  # Пропускаем заголовок

            for parts in lines:
                try:
                    record_date = datetime.datetime.strptime(parts[1], "%Y-%m-%d")
                    if start_date <= record_date <= end_date:
                        if parts[2] == "income":
                            stats["income"] += float(parts[5])
                        elif parts[2] == "expense":
                            stats["expense"] += float(parts[5])
                except ValueError:
                    continue  # Пропускаем некорректные строки
        return stats
