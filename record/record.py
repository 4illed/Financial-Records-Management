import uuid
import datetime


class Record:
    """
    Класс для представления финансовой записи.
    """

    def __init__(self, record_type, category, amount, description="", date=None):
        """
        Инициализация новой записи.

        :param record_type: Тип записи (income или expense).
        :param category: Категория записи (например, salary, food).
        :param amount: Сумма записи (положительная для доходов, отрицательная для расходов).
        :param description: Описание записи (необязательно).
        """
        self.id = str(uuid.uuid4())
        self.date = date or datetime.datetime.now().strftime("%Y-%m-%d")
        self.record_type = record_type
        self.category = category
        self.description = description
        self.amount = amount

    def to_list(self):
        """
        Преобразование записи в список для сохранения в CSV.

        :return: Список значений записи.
        """
        return [
            self.id,
            self.date,
            self.record_type,
            self.category,
            self.description,
            self.amount,
        ]
