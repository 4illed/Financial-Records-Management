import csv
import datetime

from record.record import Record


class RecordUtils:
    def add_record(file_path, record: Record):
        # Если все проверки прошли, добавляем запись в файл
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(record.to_list())

    def delete_record(file_path, record_id):
        with open(file_path, "r") as file:
            lines = list(csv.reader(file))

        # Удаляем запись с указанным ID (предполагается, что ID — это индекс записи)
        if 0 < record_id <= len(lines):
            del lines[record_id]

        # Перезаписываем файл с удалением
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lines)

    def edit_record(file_path, record_id, updated_record: Record):
        with open(file_path, "r") as file:
            lines = list(csv.reader(file))

        # Обновляем запись по ID
        if 0 < record_id <= len(lines):
            lines[record_id] = updated_record.to_list()

        # Перезаписываем файл с обновлённой записью
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lines)

    def search_records(file_path, search_term):
        results = []
        with open(file_path, "r") as file:
            lines = csv.reader(file)
            next(lines)  # Пропускаем заголовок
            for parts in lines:
                if search_term.lower() in parts[2].lower():  # Ищем по категории
                    results.append(parts)
        return results

    def calculate_statistics(file_path, start_date, end_date):
        stats = {"income": 0, "expense": 0}
        with open(file_path, "r") as file:
            lines = csv.reader(file)
            next(lines)  # Пропускаем заголовок

            # Проходим по всем строкам данных
            for parts in lines:
                try:
                    record_date = datetime.datetime.strptime(
                        parts[1], "%Y-%m-%d"
                    )  # Понимание формата
                    if start_date <= record_date <= end_date:
                        if parts[2] == "income":
                            stats["income"] += float(parts[5])
                        elif parts[2] == "expense":
                            stats["expense"] += float(parts[5])
                except ValueError:
                    continue  # Пропускаем некорректные строки
        return stats
