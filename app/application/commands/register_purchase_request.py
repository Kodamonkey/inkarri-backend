class RegisterPurchaseRequestCommand:
    def __init__(self, purchase_request_service):
        self.purchase_request_service = purchase_request_service

    def execute(self, request_name, request_number, client_name, client_address, category, required_date, due_date):
        purchase_request = self.user_service.register_user(request_name, request_number, client_name, client_address, category, required_date, due_date)
        return purchase_request
