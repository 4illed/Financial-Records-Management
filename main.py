from record.record_utils import RecordUtils
from record.record import Record
import csv

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
                record_type = input("Введите тип записи (income/expense): ").strip().lower()
                if record_type not in ['income', 'expense']:
                    print('Ошибка. Тип записи должен быть "income" или "expense".')
                    continue
                break
            category = input('Введите категорию: ')
            
            while True:
                try:
                    amount = float(input('Введите сумму: '))
                    if amount > 0 and record_type == 'income':
                        amount = -amount
                    elif amount < 0 and record_type == 'expense':
                        amount = abs(amount)
                    break
                except ValueError:
                    print('Ошибка. Ввод должен быть числом')
            
            description = input('Введите описание: ')
            # Создаем новую запись  
            new_record = Record(record_type, category, amount, description)
            file_path = input("Введите путь к файлу (по умолчанию records.csv): ")
            if not file_path:
                file_path = "records.csv"
            record_utils.add_record(record=new_record, file_path=file_path)     
        elif choice == "2":
            # Удалить запись
            try:
                record_id = input('Введите ID записи, которую хотите удалить: ')
                file_path = input("Введите путь к файлу (по умолчанию records.csv): ")
                if not file_path:
                    file_path = "records.csv"
                record_utils.delete_record(record_id, file_path)
                print('Запись успешно удалена')
            except:
                print('Произошла ошибка при удалении')      
        elif choice == "3":
            # Редактировать запись
            try:
                record_id = input('Введите ID записи, которую хотите изменить: ')
                file_path = input("Введите путь к файлу (по умолчанию records.csv): ")
                if not file_path:
                    file_path = "records.csv"
            
                with open(file_path, 'r') as file:
                    lines = list(csv.reader(file))
                found = False
                for i, line in enumerate(lines):
                    if line[0] == record_id:
                        found = True
                        print(f"Ваша текущая запись {record_id}")
                        break
                if not found:
                    print(f'Произошла ошибка. Запись в ID {record_id} не была найдена')
                    continue
                
                while True:
                    record_type = input(f"Введите тип записи (income/expense{line[2]}): ").strip().lower()
                    if record_type not in ['income', 'expense']:
                        print('Ошибка. Тип записи должен быть "income" или "expense".')
                        continue
                    break
                
                category = input(f"Введите новую категорию ({line[3]}): ").strip()
                
                description = input(f"Введите новое описание ({line[4]}): ").strip()
                
                while True:
                    try:
                        amount = float(input(f'Введите сумму ({line[5]}): '))
                        if amount > 0 and record_type == 'income':
                            amount = -amount
                        elif amount < 0 and record_type == 'expense':
                            amount = abs(amount)
                        break
                    except ValueError:
                        print('Ошибка. Ввод должен быть числом')
                        
                updated_record = Record(record_type, category, amount, description)
                updated_record.id = record_id
                updated_record.date = line[1]
                record_utils.edit_record(record_id=record_id, updated_record=updated_record, file_path=file_path)
                print('Запись успешно изменена')
            except:
                print('Произошла ошибка при изменении')
        elif choice == "4":
            # Поиск записей
            try:
                search_record = input('Введите категорию записи: ')
                file_path = input("Введите путь к файлу (по умолчанию records.csv): ")
                if not file_path:
                    file_path = "records.csv"
                results = record_utils.search_records(search_term=search_record, file_path=file_path)
                if results:
                    print('Записи под данной категории: ')
                    for result in results:
                        print(result)
                    
                else:
                    print('Записи с данной категорией отсутствуют')
            except:
                print('Произошла ошибка при поиске записей')
                
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
