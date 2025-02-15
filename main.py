from record.record_utils import RecordUtils
from record.record import Record


def main():

    record_utils = RecordUtils()

    while True:
        # Вывести список возможных действий
        print("Выберите действие:")
        print("1. Добавить запись")
        print("2. Удалить запись")
        print("3. Редактировать запись")
        print("4. Поиск записей")
        print("5. Показать статистику")
        print("6. Выйти")

        # Получить выбор пользователя
        choice = input("Введите номер действия: ")

        # Обработать выбор пользователя
        if choice == "1":
            # Добавить запись
            new_record = Record(
                input("Введите тип записи (income/expense): "),
                input("Введите категорию: "),
                # todo: добавить проверку на ввод числа
                float(input("Введите сумму: ")),
                input("Введите описание (необязательно): "),
            )
            file_path = input("Введите путь к файлу (по умолчанию records.csv): ")
            if not file_path:
                file_path = "records.csv"
            record_utils.add_record(record=new_record, file_path=file_path)
        elif choice == "2":
            # Удалить запись
            record_utils.delete_record()
        elif choice == "3":
            # Редактировать запись
            record_utils.edit_record()
        elif choice == "4":
            # Поиск записей
            record_utils.search_records()
        elif choice == "5":
            # Показать статистику
            record_utils.calculate_statistics()
        elif choice == "6":
            # Выйти
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
