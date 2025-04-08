import pytest
from domain.services.user_service import UserService
import werkzeug.security

class TestUserService:
    
    def test_register_user_with_valid_data(self, mock_user_repository):
        """Test que el registro de usuario funciona con datos válidos"""
        print("\n=== Test: Registro de usuario con datos válidos ===")
        
        # Arrange
        print("- Creando servicio de usuario con repositorio mock")
        service = UserService(mock_user_repository)
        
        print("- Preparando datos de usuario cliente")
        name = "John Doe"
        email = "john@example.com"
        password = "password123"
        role = "client"
        
        # Act
        print(f"- Registrando usuario: {name}, {email}, role={role}")
        user = service.register_user(name, email, password, role)
        
        # Assert
        print("- Verificando que el usuario fue creado correctamente")
        assert user is not None
        print(f"- Verificando nombre: {user.name}")
        assert user.name == name
        print(f"- Verificando email: {user.email}")
        assert user.email == email
        print(f"- Verificando rol: {user.role}")
        assert user.role == role
        print(f"- Verificando estado: {user.status}")
        assert user.status == "pending"  # RN01: Usuario comienza como pendiente
        print("- Verificando que la contraseña fue cifrada")
        assert werkzeug.security.check_password_hash(user.password, password)
        print("- Verificando que se llamó al método save del repositorio")
        mock_user_repository.save.assert_called_once()
        print("✓ Test completado con éxito\n")
    
    def test_register_user_with_invalid_role(self, mock_user_repository):
        """Test que valida que el rol sea válido"""
        print("\n=== Test: Registro de usuario con rol inválido ===")
        
        # Arrange
        print("- Creando servicio de usuario con repositorio mock")
        service = UserService(mock_user_repository)
        
        print("- Preparando datos de usuario con rol inválido")
        name = "John Doe"
        email = "john@example.com"
        password = "password123"
        invalid_role = "invalid_role"
        
        # Act & Assert
        print(f"- Intentando registrar usuario con rol inválido: {invalid_role}")
        with pytest.raises(ValueError) as excinfo:
            service.register_user(name, email, password, invalid_role)
        
        print(f"- Verificando mensaje de error: {str(excinfo.value)}")
        assert "Invalid input data" in str(excinfo.value)
        print("- Verificando que no se llamó al método save del repositorio")
        mock_user_repository.save.assert_not_called()
        print("✓ Test completado con éxito\n")
    
    def test_change_user_status_with_valid_data(self, mock_user_repository):
        """Test que el cambio de estado funciona correctamente"""
        print("\n=== Test: Cambio de estado de usuario ===")
        
        # Arrange
        print("- Creando servicio de usuario con repositorio mock")
        service = UserService(mock_user_repository)
        
        print("- Registrando un usuario en estado 'pending'")
        user = service.register_user("John Doe", "john@example.com", "password123", "client")
        print(f"- Usuario creado con ID: {user.user_id} y estado: {user.status}")
        
        # Act
        print(f"- Cambiando estado del usuario a 'approved'")
        updated_user = service.change_user_status(user.user_id, "approved")
        
        # Assert
        print(f"- Verificando que el estado cambió a 'approved'")
        assert updated_user.status == "approved"
        print("- Verificando que se llamó al método update del repositorio")
        mock_user_repository.update.assert_called_once()
        print("✓ Test completado con éxito\n")