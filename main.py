import csv
import datetime
import sys
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
            while True:
                record_type = (
                    input("Введите тип записи (income/expense): ").strip().lower()
                )
                if record_type not in ["income", "expense"]:
                    print('Ошибка. Тип записи должен быть "income" или "expense".')
                    continue
                break
            category = input("Введите категорию: ")

            while True:
                try:
                    amount = float(input("Введите сумму: "))
                    if record_type == "expense":
                        amount = -abs(amount)
                    else:
                        amount = abs(amount)
                    break
                except ValueError:
                    print("Ошибка. Ввод должен быть числом")

            description = input("Введите описание: ")
            # Создаем новую запись
            new_record = Record(record_type, category, amount, description)
            file_path = input("Введите путь к файлу (по умолчанию records.csv): ")
            if not file_path or file_path.isspace():
                file_path = "records.csv"
            record_utils.add_record(record=new_record, file_path=file_path)
        elif choice == "2":
            try:
                uuid = input("Введите UUID записи для удаления: ").strip()
                file_path = (
                    input("Введите путь к файлу (по умолчанию records.csv): ")
                    or "records.csv"
                )

                if RecordUtils.delete_record(uuid, file_path):
                    print(" Запись успешно удалена")
                else:
                    print("Запись не найдена или произошла ошибка")

            except Exception as e:
                print(f"Произошла ошибка: {e}")
        elif choice == "3":
            # Редактировать запись
            try:
                record_id = input("Введите ID записи, которую хотите изменить: ")
                file_path = input("Введите путь к файлу (по умолчанию records.csv): ")
                if not file_path:
                    file_path = "records.csv"

                with open(file_path, "r") as file:
                    lines = list(csv.reader(file))
                found = False
                for line in lines:
                    if line[0] == record_id:
                        found = True
                        print(f"Ваша текущая запись {record_id}")
                        break
                if not found:
                    print(f"Произошла ошибка. Запись в ID {record_id} не была найдена")
                    continue

                while True:
                    record_type = (
                        input(f"Введите тип записи (income/expense{line[2]}): ")
                        .strip()
                        .lower()
                    )
                    if record_type not in ["income", "expense"]:
                        print('Ошибка. Тип записи должен быть "income" или "expense".')
                        continue
                    break

                category = input(f"Введите новую категорию ({line[3]}): ").strip()

                description = input(f"Введите новое описание ({line[4]}): ").strip()

                while True:
                    try:
                        amount = float(input(f"Введите сумму ({line[5]}): "))
                        if amount > 0 and record_type == "income":
                            amount = -amount
                        elif amount < 0 and record_type == "expense":
                            amount = abs(amount)
                        break
                    except ValueError:
                        print("Ошибка. Ввод должен быть числом")

                updated_record = Record(record_type, category, amount, description)
                updated_record.id = record_id
                updated_record.date = line[1]
                record_utils.edit_record(
                    record_id=record_id,
                    updated_record=updated_record,
                    file_path=file_path,
                )
                print("Запись успешно изменена")
            except Exception as e:
                print(f"Произошла ошибка при изменении: {e}")
        elif choice == "4":
            # Поиск записей
            try:
                search_record = input("Введите категорию записи: ")
                file_path = input("Введите путь к файлу (по умолчанию records.csv): ")
                if not file_path:
                    file_path = "records.csv"
                results = record_utils.search_records(
                    search_term=search_record, file_path=file_path
                )
                if results:
                    print("Записи под данной категории: ")
                    for result in results:
                        print(result)

                else:
                    print("Записи с данной категорией отсутствуют")
            except Exception as e:
                print(f"Произошла ошибка при поиске записей: {e}")

        elif choice == "5":
            # Показать статистику
            try:
                start_date_str = input("Введите начальную дату (YYYY-MM-DD): ").strip()
                end_date_str = input("Введите конечную дату (YYYY-MM-DD): ").strip()

                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
                file_path = input("Введите путь к файлу (по умолчанию records.csv): ")
                if not file_path:
                    file_path = "records.csv"

                stats = record_utils.calculate_statistics(
                    start_date=start_date, end_date=end_date, file_path=file_path
                )
                print(f"Общая сумма доходов {stats['income']}")
                print(f"Общая сумма расходов {stats['expense']}")

                print("Доходы по категориям")
                for category, amount in stats["income"]:
                    print(f"Категория {category}, доход {amount}")

                print("Расходы по категориям")
                for category, amount in stats["expense"]:
                    print(f"Категория {category}, расход {amount}")
            except Exception as e:
                print("Произошла ошибка при расчете статистики")
                print(f"Ошибка: {e}", file=sys.stderr)

        elif choice == "6":
            # Выйти
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
