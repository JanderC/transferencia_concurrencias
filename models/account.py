class Account:
    def __init__(self, id=None, name=None, balance=0.0, created_at=None):
        self.id = id
        self.name = name
        self.balance = balance
        self.created_at = created_at

    @staticmethod
    def from_db_row(row):
        return Account(
            id=row[0],
            name=row[1],
            balance=row[2],
            created_at=row[3]
        )