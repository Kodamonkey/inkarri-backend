
class RegisterUserCommand:
    def __init__(self, user_service):
        self.user_service = user_service

    def execute(self, name, email, password, role):
        user = self.user_service.register_user(name, email, password, role)
        return user
