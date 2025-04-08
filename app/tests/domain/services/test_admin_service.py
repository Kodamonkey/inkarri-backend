import pytest
from domain.services.admin_service import AdminService
from domain.services.user_service import UserService

class TestAdminService:
    
    def test_approve_user_by_admin(self, mock_user_repository):
        """Test que un administrador puede aprobar un usuario (RN03)"""
        print("\n=== Test: Aprobación de usuario por administrador ===")
        
        # Arrange
        print("- Creando servicios de admin y usuario con repositorio mock")
        admin_service = AdminService(mock_user_repository)
        user_service = UserService(mock_user_repository)
        
        print("- Creando un usuario cliente en estado 'pending'")
        user = user_service.register_user("John Doe", "john@example.com", "password123", "client")
        print(f"- Usuario creado con ID: {user.user_id} y estado: {user.status}")
        
        admin_id = "admin1"  # ID del admin creado en el fixture
        print(f"- Usando administrador con ID: {admin_id}")
        
        # Act
        print(f"- Administrador aprobando al usuario")
        approved_user = admin_service.approve_user(admin_id, user.user_id)
        
        # Assert
        print(f"- Verificando que el estado cambió a 'approved'")
        assert approved_user.status == "approved"
        print("- Verificando que se llamó al método update del repositorio")
        mock_user_repository.update.assert_called()
        print("✓ Test completado con éxito - RN03 verificada\n")
    
    def test_reject_user_by_admin(self, mock_user_repository):
        """Test que un administrador puede rechazar un usuario (RN03)"""
        print("\n=== Test: Rechazo de usuario por administrador ===")
        
        # Arrange
        print("- Creando servicios de admin y usuario con repositorio mock")
        admin_service = AdminService(mock_user_repository)
        user_service = UserService(mock_user_repository)
        
        print("- Creando un usuario cliente en estado 'pending'")
        user = user_service.register_user("John Doe", "john@example.com", "password123", "client")
        print(f"- Usuario creado con ID: {user.user_id} y estado: {user.status}")
        
        admin_id = "admin1"  # ID del admin creado en el fixture
        print(f"- Usando administrador con ID: {admin_id}")
        
        reason = "Datos incorrectos"
        print(f"- Razón de rechazo: '{reason}'")
        
        # Act
        print(f"- Administrador rechazando al usuario")
        rejected_user = admin_service.reject_user(admin_id, user.user_id, reason)
        
        # Assert
        print(f"- Verificando que el estado cambió a 'rejected'")
        assert rejected_user.status == "rejected"
        print("- Verificando que se llamó al método update del repositorio")
        mock_user_repository.update.assert_called()
        print("✓ Test completado con éxito - RN03 verificada\n")
    
    def test_non_admin_cannot_approve_user(self, mock_user_repository):
        """Test que solo un administrador puede aprobar usuarios (RN03)"""
        print("\n=== Test: Usuario no-admin intenta aprobar a otro usuario ===")
        
        # Arrange
        print("- Creando servicios de admin y usuario con repositorio mock")
        admin_service = AdminService(mock_user_repository)
        user_service = UserService(mock_user_repository)
        
        print("- Creando dos usuarios cliente")
        user1 = user_service.register_user("John Doe", "john@example.com", "password123", "client")
        print(f"- Usuario 1 creado con ID: {user1.user_id} y rol: {user1.role}")
        
        user2 = user_service.register_user("Jane Smith", "jane@example.com", "password456", "client")
        print(f"- Usuario 2 creado con ID: {user2.user_id} y rol: {user2.role}")
        
        # Act & Assert
        print(f"- Usuario 1 (no-admin) intenta aprobar al Usuario 2")
        with pytest.raises(PermissionError) as excinfo:
            admin_service.approve_user(user1.user_id, user2.user_id)
        
        print(f"- Verificando mensaje de error: {str(excinfo.value)}")
        assert "Only administrators can approve users" in str(excinfo.value)
        print("✓ Test completado con éxito - RN03 verificada\n")