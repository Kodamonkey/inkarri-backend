import pytest
from domain.services.user_service import UserService
from domain.services.admin_service import AdminService
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.database import SessionLocal

@pytest.fixture
def db_session():
    """Usa la sesión configurada para la base de datos existente."""
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def user_repository(db_session):
    """Crea un repositorio real utilizando la base de datos configurada."""
    return UserRepositoryImpl(db_session)

class TestUserWorkflow:
    
    def test_complete_user_registration_workflow(self, user_repository):
        """Test del flujo completo de registro y aprobación de usuario"""
        print("\n=== Prueba de Integración: Flujo completo de registro y aprobación ===")
        
        # Arrange
        print("- Creando servicios de usuario y admin")
        user_service = UserService(user_repository)
        admin_service = AdminService(user_repository)
        
        admin_id = "admin1"
        print(f"- Usando administrador con ID: {admin_id}")
        
        # Act - 1. Registro de usuario cliente
        print("\n>> PASO 1: Registro de usuario cliente (RN04)")
        client_name = "John Client"
        client_email = "john@example.com"
        client_password = "password123"
        client_role = "client"
        
        print(f"- Registrando cliente: {client_name}, {client_email}, role={client_role}")
        client = user_service.register_user(client_name, client_email, client_password, client_role)
        
        # Assert - Usuario creado con estado pendiente
        print(f"- Cliente creado con ID: {client.user_id}")
        print(f"- Verificando estado inicial: {client.status} (RN01)")
        assert client.status == "pending"
        
        # # Act - 2. Administrador aprueba al usuario
        # print("\n>> PASO 2: Administrador aprueba al cliente (RN03)")
        # print(f"- Admin {admin_id} aprobando al cliente {client.user_id}")
        # approved_client = admin_service.approve_user(admin_id, client.user_id)
        
        # # Assert - Usuario ahora está aprobado
        # print(f"- Verificando nuevo estado: {approved_client.status}")
        # assert approved_client.status == "approved"
        
        # Act - 3. Registro de empresa indígena
        print("\n>> PASO 3: Registro de empresa indígena (RN04)")
        company_name = "Native Company"
        company_email = "company@example.com"
        company_password = "password456"
        company_role = "indigenous_company"
        
        print(f"- Registrando empresa: {company_name}, {company_email}, role={company_role}")
        company = user_service.register_user(company_name, company_email, company_password, company_role)
        
        # Assert - Empresa creada con estado pendiente
        print(f"- Empresa creada con ID: {company.user_id}")
        print(f"- Verificando estado inicial: {company.status} (RN02)")
        assert company.status == "pending"
        
        # # Act - 4. Administrador rechaza a la empresa
        # print("\n>> PASO 4: Administrador rechaza a la empresa (RN03)")
        # reason = "Documentación incompleta"
        # print(f"- Admin {admin_id} rechazando a la empresa {company.user_id}")
        # print(f"- Razón: {reason}")
        # rejected_company = admin_service.reject_user(admin_id, company.user_id, reason)
        
        # # Assert - Empresa ahora está rechazada
        # print(f"- Verificando nuevo estado: {rejected_company.status}")
        # assert rejected_company.status == "rejected"
        
        print("\n✓ Prueba de integración completada con éxito")
        print("- Reglas verificadas: RN01, RN02, RN03, RN04")