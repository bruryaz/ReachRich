class Action:
    def __init__(self, id, user_id, action_type, amount, timestamp):
        self.id = id
        self.user_id = user_id
        self.action_type = action_type
        self.amount = amount
        self.timestamp = timestamp