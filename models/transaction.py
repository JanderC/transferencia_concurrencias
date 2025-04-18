class Transaction:
    def __init__(self, id=None, account_id=None, recipient_id=None, 
                 amount=0.0, transaction_type=None, status=None, created_at=None):
        self.id = id
        self.account_id = account_id
        self.recipient_id = recipient_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.status = status
        self.created_at = created_at

    @staticmethod
    def from_db_row(row):
        return Transaction(
            id=row[0],
            account_id=row[1],
            recipient_id=row[2],
            amount=row[3],
            transaction_type=row[4],
            status=row[5],
            created_at=row[6]
        )