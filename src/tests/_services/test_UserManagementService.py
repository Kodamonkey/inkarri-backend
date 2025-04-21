import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import bcrypt
from datetime import datetime

# Agregar directorio raíz al path para permitir las importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Importar el servicio a probar
from src.services.UserManagementService import AdminManagementService
from src.models.User import User
from src.models.Client import Client
from src.models.Company import Company

class TestUserManagementService(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear mocks para los datos de usuarios
        self.client_data = {
            'username': 'test_client',
            'email': 'test_client@example.com',
            'password': 'secure_password',
            'subscription': 'free'
        }
        
        self.company_data = {
            'username': 'test_company',
            'email': 'test_company@example.com', 
            'password': 'secure_password',
            'categories_id': 1
        }
        
        self.admin_data = {
            'username': 'test_admin',
            'email': 'test_admin@example.com',
            'password': 'admin_password'
        }
        
        # Mock del cliente para simulaciones
        self.mock_client = {
            'id': 1,
            'username': 'test_client',
            'email': 'test_client@example.com',
            'status': 'pending',
            'access': 'client',
            'subscription': 'free'
        }
        
        # Mock de la empresa para simulaciones
        self.mock_company = {
            'id': 1,
            'username': 'test_company', 
            'email': 'test_company@example.com',
            'status': 'pending',
            'access': 'company',
            'categories_id': 1
        }
        
        # Mock del admin para simulaciones
        self.mock_admin = {
            'id': 1,
            'username': 'test_admin',
            'email': 'test_admin@example.com',
            'status': 'approved',
            'access': 'admin'
        }

    @patch('src.models.Client.Client.get_by_email')
    @patch('src.models.Client.Client.create')
    @patch('src.models.Client.Client.update')
    def test_register_client_success(self, mock_update, mock_create, mock_get_by_email):
        """Prueba el registro exitoso de un cliente"""
        # Configurar el mock para simular que no existe un cliente con ese email
        mock_get_by_email.return_value = None
        # Configurar el mock para simular un registro exitoso
        mock_create.return_value = 1
        mock_update.return_value = True
        
        # Ejecutar la función a probar
        result = AdminManagementService.register_client(self.client_data)
        
        # Verificar que se llamaron los métodos esperados
        mock_get_by_email.assert_called_once_with(self.client_data['email'])
        mock_create.assert_called_once()
        mock_update.assert_called_once()
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertEqual(result['client_id'], 1)
        self.assertEqual(result['status_code'], 201)

    @patch('src.models.Client.Client.get_by_email')
    def test_register_client_existing_email(self, mock_get_by_email):
        """Prueba el registro de un cliente con email ya existente"""
        # Configurar el mock para simular que ya existe un cliente con ese email
        mock_get_by_email.return_value = {'id': 1, 'email': self.client_data['email']}
        
        # Ejecutar la función a probar
        result = AdminManagementService.register_client(self.client_data)
        
        # Verificar que se llamó el método esperado
        mock_get_by_email.assert_called_once_with(self.client_data['email'])
        
        # Verificar resultado
        self.assertFalse(result['success'])
        self.assertEqual(result['status_code'], 409)
        self.assertIn('Ya existe', result['message'])

    @patch('src.models.Company.Company.get_by_email')
    @patch('src.models.Company.Company.create')
    @patch('src.models.Company.Company.update')
    def test_register_company_success(self, mock_update, mock_create, mock_get_by_email):
        """Prueba el registro exitoso de una empresa"""
        # Configurar los mocks
        mock_get_by_email.return_value = None
        mock_create.return_value = 1
        mock_update.return_value = True
        
        # Ejecutar la función a probar
        result = AdminManagementService.register_company(self.company_data)
        
        # Verificar que se llamaron los métodos esperados
        mock_get_by_email.assert_called_once_with(self.company_data['email'])
        mock_create.assert_called_once()
        mock_update.assert_called_once()
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertEqual(result['company_id'], 1)
        self.assertEqual(result['status_code'], 201)

    @patch('src.models.User.User.get_by_id')
    @patch('src.models.Client.Client.get_by_id')
    @patch('src.models.Client.Client.update')
    @patch('src.services.UserManagementService.AdminManagementService._log_admin_action')
    def test_approve_client_success(self, mock_log, mock_update, mock_get_client, mock_get_admin):
        """Prueba la aprobación exitosa de un cliente"""
        # Configurar los mocks
        mock_get_admin.return_value = self.mock_admin
        mock_get_client.return_value = self.mock_client
        mock_update.return_value = True
        mock_log.return_value = None
        
        # Ejecutar la función a probar
        result = AdminManagementService.approve_client(1, 1)
        
        # Verificar que se llamaron los métodos esperados
        mock_get_admin.assert_called_once_with(1)
        mock_get_client.assert_called_once_with(1)
        mock_update.assert_called_once()
        mock_log.assert_called_once()
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertEqual(result['status_code'], 200)

    @patch('src.models.User.User.get_by_id')
    def test_approve_client_not_admin(self, mock_get_admin):
        """Prueba que solo administradores pueden aprobar clientes"""
        # Configurar los mocks para simular un usuario que no es admin
        mock_get_admin.return_value = {'id': 2, 'access': 'client'}
        
        # Ejecutar la función a probar
        result = AdminManagementService.approve_client(2, 1)
        
        # Verificar resultado
        self.assertFalse(result['success'])
        self.assertEqual(result['status_code'], 403)
        self.assertIn('Solo los administradores', result['message'])

    @patch('src.models.User.User.get_by_id')
    @patch('src.models.Company.Company.get_by_id')
    @patch('src.models.Company.Company.update')
    @patch('src.services.UserManagementService.AdminManagementService._log_admin_action')
    def test_approve_company_success(self, mock_log, mock_update, mock_get_company, mock_get_admin):
        """Prueba la aprobación exitosa de una empresa"""
        # Configurar los mocks
        mock_get_admin.return_value = self.mock_admin
        mock_get_company.return_value = self.mock_company
        mock_update.return_value = True
        mock_log.return_value = None
        
        # Ejecutar la función a probar
        result = AdminManagementService.approve_company(1, 1)
        
        # Verificar que se llamaron los métodos esperados
        mock_get_admin.assert_called_once_with(1)
        mock_get_company.assert_called_once_with(1)
        mock_update.assert_called_once()
        mock_log.assert_called_once()
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertEqual(result['status_code'], 200)

    @patch('src.models.User.User.get_by_id')
    @patch('src.models.Client.Client.get_by_id')
    @patch('src.models.Client.Client.update')
    @patch('src.services.UserManagementService.AdminManagementService._log_admin_action')
    def test_reject_client_success(self, mock_log, mock_update, mock_get_client, mock_get_admin):
        """Prueba el rechazo exitoso de un cliente"""
        # Configurar los mocks
        mock_get_admin.return_value = self.mock_admin
        mock_get_client.return_value = self.mock_client
        mock_update.return_value = True
        mock_log.return_value = None
        
        # Ejecutar la función a probar
        result = AdminManagementService.reject_client(1, 1, "No cumple requisitos")
        
        # Verificar que se llamaron los métodos esperados
        mock_get_admin.assert_called_once_with(1)
        mock_get_client.assert_called_once_with(1)
        mock_update.assert_called_once()
        mock_log.assert_called_once()
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertEqual(result['status_code'], 200)

    @patch('src.models.User.User.authenticate')
    def test_authenticate_admin_success(self, mock_authenticate):
        """Prueba la autenticación exitosa de un administrador"""
        # Configurar el mock para devolver un administrador aprobado
        mock_authenticate.return_value = {
            'id': 1,
            'username': 'test_admin',
            'email': 'test_admin@example.com',
            'access': 'admin',
            'status': 'approved'
        }
        
        # Ejecutar la función a probar
        result = AdminManagementService.authenticate('test_admin@example.com', 'admin_password')
        
        # Verificar que se llamó el método esperado
        mock_authenticate.assert_called_once_with('test_admin@example.com', 'admin_password')
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertEqual(result['user_type'], 'admin')
        self.assertEqual(result['status_code'], 200)

    @patch('src.models.User.User.authenticate')
    @patch('src.models.Client.Client.authenticate')
    def test_authenticate_client_pending(self, mock_client_auth, mock_admin_auth):
        """Prueba la autenticación de un cliente pendiente de aprobación"""
        # Configurar los mocks
        mock_admin_auth.return_value = None
        mock_client_auth.return_value = {
            'id': 1,
            'username': 'test_client',
            'email': 'test_client@example.com',
            'access': 'client',
            'status': 'pending'
        }
        
        # Ejecutar la función a probar
        result = AdminManagementService.authenticate('test_client@example.com', 'client_password')
        
        # Verificar resultado
        self.assertFalse(result['success'])
        self.assertEqual(result['status_code'], 403)
        self.assertIn('pendiente de aprobación', result['message'])

    @patch('src.models.User.User.authenticate')
    @patch('src.models.Client.Client.authenticate')
    @patch('src.models.Company.Company.authenticate')
    def test_authenticate_company_approved(self, mock_company_auth, mock_client_auth, mock_admin_auth):
        """Prueba la autenticación exitosa de una empresa aprobada"""
        # Configurar los mocks
        mock_admin_auth.return_value = None
        mock_client_auth.return_value = None
        mock_company_auth.return_value = {
            'id': 1,
            'username': 'test_company',
            'email': 'test_company@example.com',
            'access': 'company',
            'status': 'approved',
            'categories_id': 1
        }
        
        # Ejecutar la función a probar
        result = AdminManagementService.authenticate('test_company@example.com', 'company_password')
        
        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertEqual(result['user_type'], 'company')
        self.assertEqual(result['status_code'], 200)

    @patch('src.models.Client.Client.get_connection')
    def test_get_pending_clients(self, mock_get_connection):
        """Prueba obtener la lista de clientes pendientes"""
        # Crear un mock para cursor y conexión
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'username': 'client1', 'status': 'pending'},
            {'id': 2, 'username': 'client2', 'status': 'pending'}
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        
        # Ejecutar la función a probar
        result = AdminManagementService.get_pending_clients()
        
        # Verificar que se llamó el método esperado
        mock_get_connection.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        
        # Verificar resultado
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['status'], 'pending')

    @patch('src.models.Company.Company.get_connection')
    def test_get_pending_companies(self, mock_get_connection):
        """Prueba obtener la lista de empresas pendientes"""
        # Crear un mock para cursor y conexión
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'username': 'company1', 'status': 'pending'},
            {'id': 2, 'username': 'company2', 'status': 'pending'}
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        
        # Ejecutar la función a probar
        result = AdminManagementService.get_pending_companies()
        
        # Verificar que se llamó el método esperado
        mock_get_connection.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        
        # Verificar resultado
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['status'], 'pending')

    @patch('src.models.User.User.get_connection')
    def test_log_admin_action(self, mock_get_connection):
        """Prueba el registro de acciones administrativas"""
        # Crear un mock para cursor y conexión
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        
        # Ejecutar la función a probar
        AdminManagementService._log_admin_action(
            admin_id=1, 
            action="test_action",
            entity_id=2,
            details="Prueba de registro de acción"
        )
        
        # Verificar que se llamaron los métodos esperados
        mock_get_connection.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()