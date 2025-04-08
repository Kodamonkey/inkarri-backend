# filepath: c:\Users\sebas\Desktop\inkarri-backend\app\domain\services\admin_service.py
from domain.repositories.user_repository import UserRepository
from domain.entities.user import User

class AdminService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def approve_user(self, admin_id, user_id):
        # Verificar que quien aprueba sea administrador
        admin = self.user_repository.get_by_id(admin_id)
        if not admin or admin.role != 'admin':
            raise PermissionError("Only administrators can approve users")
        
        return self._change_user_status(user_id, 'approved')
    
    def reject_user(self, admin_id, user_id, reason=None):
        # Verificar que quien rechaza sea administrador
        admin = self.user_repository.get_by_id(admin_id)
        if not admin or admin.role != 'admin':
            raise PermissionError("Only administrators can reject users")
        
        return self._change_user_status(user_id, 'rejected')
    
    def _change_user_status(self, user_id, status):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if status == 'approved':
            user.approve()
        elif status == 'rejected':
            user.reject()
        
        self.user_repository.update(user)
        return user