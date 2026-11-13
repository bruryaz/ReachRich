class Category:
    def __init__(self, id, user_id , category_name, transaction_type, parent_id, is_system, is_active, created_at):
        self.id = id
        self.user_id = user_id
        self.name = category_name
        self.transaction_type = transaction_type
        self.parent_id = parent_id
        self.is_system = is_system
        self.is_active = is_active
        self.created_at = created_at