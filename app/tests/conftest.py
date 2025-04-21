# import pytest
# from app.database import SessionLocal
# from domain.repositories.user_repository import UserRepository
# from domain.entities.user import User

# @pytest.fixture
# def mock_user_repository():
#     """Fixture that creates a mock user repository"""
#     repository = SessionLocal(spec=UserRepository)
    
#     # Simulamos una base de datos en memoria
#     users_db = {}
    
#     # Mock para el método save
#     def mock_save(user):
#         if user.user_id is None:
#             user.user_id = str(len(users_db) + 1)
#         users_db[user.user_id] = user
#         return user
    
#     # Mock para get_by_id
#     def mock_get_by_id(user_id):
#         return users_db.get(user_id)
    
#     # Mock para update
#     def mock_update(user):
#         if user.user_id in users_db:
#             users_db[user.user_id] = user
#             return user
#         return None
    
#     # Mock para get_by_email
#     def mock_get_by_email(email):
#         for user in users_db.values():
#             if user.email == email:
#                 return user
#         return None
    
#     # Configuramos los mocks en el repositorio
#     repository.save.side_effect = mock_save
#     repository.get_by_id.side_effect = mock_get_by_id
#     repository.update.side_effect = mock_update
#     repository.get_by_email.side_effect = mock_get_by_email
    
#     # Creamos unos usuarios predefinidos para pruebas
#     admin = User(name="Admin User", email="admin@example.com", 
#                 password="hashed_password", role="admin", status="approved")
#     users_db[admin.user_id] = admin
    
#     return repository