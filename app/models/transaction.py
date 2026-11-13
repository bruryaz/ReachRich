class Transaction:
    def __init__(self, id, account_id, category_id, transaction_type, description, transaction_date, created_at, action_type, amount, timestamp):
        self.id = id
        self.account_id = account_id
        self.category_id = category_id
        self.transaction_type = transaction_type
        self.description = description
        self.created_at = created_at
        self.transaction_date = transaction_date
        self.action_type = action_type
        self.amount = amount
        self.timestamp = timestamp