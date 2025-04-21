
class ChangeUserStatusCommand:
    def __init__(self, user_service):
        self.user_service = user_service

    def execute(self, user_id, status):
        user = self.user_service.change_user_status(user_id, status)
        return user
