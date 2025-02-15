import uuid


class Record:
    def __init__(self, date, record_type, category, amount, description=""):
        self.id = str(uuid.uuid4())
        self.date = date
        self.record_type = record_type
        self.category = category
        self.description = description
        self.amount = amount

    def to_list(self):
        return [
            self.id,
            self.date,
            self.record_type,
            self.category,
            self.description,
            self.amount,
        ]
