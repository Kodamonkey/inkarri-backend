from src.models.User import User
from src.models.Client import Client
from src.models.Company import Company
import bcrypt
from datetime import datetime

class UserManagementService:
    """
    Servicio para gestionar usuarios, implementando las reglas de negocio relacionadas
    con la administración de usuarios, clientes y empresas.
    """
    
    # Constantes para los estados de usuario
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    
    # Constantes para los roles de usuario
    ROLE_ADMIN = 'admin'
    ROLE_CLIENT = 'client'
    ROLE_COMPANY = 'company'
    
    @staticmethod
    def register_client(client_data):
        """
        Registra un nuevo cliente en el sistema
        
        Args:
            client_data: Datos del cliente a registrar
            
        Returns:
            dict: Resultado de la operación con mensaje y estado
        """
        try:
            # Validar si ya existe un cliente con ese email
            existing_client = Client.get_by_email(client_data.get('email'))
            if existing_client:
                return {
                    'success': False,
                    'message': 'Ya existe un cliente con ese correo electrónico',
                    'status_code': 409
                }
            
            # Crear nuevo cliente con estado pendiente
            new_client = Client(
                username=client_data.get('username'),
                email=client_data.get('email'),
                password=client_data.get('password'),
                access=UserManagementService.ROLE_CLIENT,
                subscription=client_data.get('subscription', 'free'),
                status=UserManagementService.STATUS_PENDING  # Estado inicial: pendiente
            )
            
            client_id = new_client.create()
            
            if client_id:
                # Implementación de RN01: Cliente creado con estado pendiente
                return {
                    'success': True,
                    'message': 'Cliente registrado correctamente. Su cuenta está pendiente de aprobación por un administrador.',
                    'client_id': client_id,
                    'status_code': 201
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al registrar el cliente',
                    'status_code': 500
                }
        except Exception as e:
            print(f"Error en registro de cliente: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def register_company(company_data):
        """
        Registra una nueva empresa en el sistema
        
        Args:
            company_data: Datos de la empresa a registrar
            
        Returns:
            dict: Resultado de la operación con mensaje y estado
        """
        try:
            # Validar si ya existe una empresa con ese email
            existing_company = Company.get_by_email(company_data.get('email'))
            if existing_company:
                return {
                    'success': False,
                    'message': 'Ya existe una empresa con ese correo electrónico',
                    'status_code': 409
                }
            
            # Crear nueva empresa con estado pendiente
            new_company = Company(
                username=company_data.get('username'),
                email=company_data.get('email'),
                password=company_data.get('password'),
                access=UserManagementService.ROLE_COMPANY,
                categories_id=company_data.get('categories_id'),
                status=UserManagementService.STATUS_PENDING  # Estado inicial: pendiente
            )
            
            company_id = new_company.create()
            
            if company_id:
                # Implementación de RN02: Empresa creada con estado pendiente
                return {
                    'success': True,
                    'message': 'Empresa registrada correctamente. Su cuenta está pendiente de validación por un administrador.',
                    'company_id': company_id,
                    'status_code': 201
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al registrar la empresa',
                    'status_code': 500
                }
        except Exception as e:
            print(f"Error en registro de empresa: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def register_admin(admin_data):
        """
        Registra un nuevo administrador en el sistema
        * Esta función debería estar muy restringida *
        
        Args:
            admin_data: Datos del administrador a registrar
            
        Returns:
            dict: Resultado de la operación con mensaje y estado
        """
        try:
            # Validar si ya existe un usuario con ese email
            existing_user = User.get_by_email(admin_data.get('email'))
            if existing_user:
                return {
                    'success': False,
                    'message': 'Ya existe un usuario con ese correo electrónico',
                    'status_code': 409
                }
            
            # Crear nuevo administrador (ya aprobado)
            new_admin = User(
                name=admin_data.get('name'),
                email=admin_data.get('email'),
                password=admin_data.get('password'),
                role=UserManagementService.ROLE_ADMIN,  # Rol administrador
                status=UserManagementService.STATUS_APPROVED  # Administradores ya aprobados
            )
            
            admin_id = new_admin.create()
            
            if admin_id:
                return {
                    'success': True,
                    'message': 'Administrador registrado correctamente.',
                    'admin_id': admin_id,
                    'status_code': 201
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al registrar el administrador',
                    'status_code': 500
                }
        except Exception as e:
            print(f"Error en registro de administrador: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def approve_client(admin_id, client_id):
        """
        Aprueba un cliente pendiente (RN01, RN03)
        
        Args:
            admin_id: ID del administrador que realiza la acción
            client_id: ID del cliente a aprobar
            
        Returns:
            dict: Resultado de la operación con mensaje y estado
        """
        try:
            # Verificar que quien aprueba es un administrador
            admin = User.get_by_id(admin_id)
            if not admin or admin.get('role') != UserManagementService.ROLE_ADMIN:
                return {
                    'success': False,
                    'message': 'Solo los administradores pueden aprobar clientes',
                    'status_code': 403
                }
            
            # Obtener el cliente
            client = Client.get_by_id(client_id)
            if not client:
                return {
                    'success': False,
                    'message': 'Cliente no encontrado',
                    'status_code': 404
                }
            
            # Actualizar estado a aprobado
            result = Client.update(client_id, {'status': UserManagementService.STATUS_APPROVED})
            
            if result:
                return {
                    'success': True,
                    'message': 'Cliente aprobado correctamente',
                    'status_code': 200
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al aprobar el cliente',
                    'status_code': 500
                }
        except Exception as e:
            print(f"Error al aprobar cliente: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def reject_client(admin_id, client_id, reason=None):
        """
        Rechaza un cliente pendiente (RN03)
        
        Args:
            admin_id: ID del administrador que realiza la acción
            client_id: ID del cliente a rechazar
            reason: Motivo del rechazo
            
        Returns:
            dict: Resultado de la operación con mensaje y estado
        """
        try:
            # Verificar que quien rechaza es un administrador
            admin = User.get_by_id(admin_id)
            if not admin or admin.get('role') != UserManagementService.ROLE_ADMIN:
                return {
                    'success': False,
                    'message': 'Solo los administradores pueden rechazar clientes',
                    'status_code': 403
                }
            
            # Obtener el cliente
            client = Client.get_by_id(client_id)
            if not client:
                return {
                    'success': False,
                    'message': 'Cliente no encontrado',
                    'status_code': 404
                }
            
            # Actualizar estado a rechazado
            update_data = {
                'status': UserManagementService.STATUS_REJECTED
            }
            
            if reason:
                # Si el modelo Client tiene un campo para almacenar el motivo de rechazo
                update_data['rejection_reason'] = reason
                
            result = Client.update(client_id, update_data)
            
            if result:
                return {
                    'success': True,
                    'message': 'Cliente rechazado correctamente',
                    'status_code': 200
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al rechazar el cliente',
                    'status_code': 500
                }
        except Exception as e:
            print(f"Error al rechazar cliente: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def approve_company(admin_id, company_id):
        """
        Aprueba una empresa pendiente (RN02, RN03)
        
        Args:
            admin_id: ID del administrador que realiza la acción
            company_id: ID de la empresa a aprobar
            
        Returns:
            dict: Resultado de la operación con mensaje y estado
        """
        try:
            # Verificar que quien aprueba es un administrador
            admin = User.get_by_id(admin_id)
            if not admin or admin.get('role') != UserManagementService.ROLE_ADMIN:
                return {
                    'success': False,
                    'message': 'Solo los administradores pueden aprobar empresas',
                    'status_code': 403
                }
            
            # Obtener la empresa
            company = Company.get_by_id(company_id)
            if not company:
                return {
                    'success': False,
                    'message': 'Empresa no encontrada',
                    'status_code': 404
                }
            
            # Actualizar estado a aprobado
            result = Company.update(company_id, {'status': UserManagementService.STATUS_APPROVED})
            
            if result:
                return {
                    'success': True,
                    'message': 'Empresa aprobada correctamente',
                    'status_code': 200
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al aprobar la empresa',
                    'status_code': 500
                }
        except Exception as e:
            print(f"Error al aprobar empresa: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def reject_company(admin_id, company_id, reason=None):
        """
        Rechaza una empresa pendiente (RN03)
        
        Args:
            admin_id: ID del administrador que realiza la acción
            company_id: ID de la empresa a rechazar
            reason: Motivo del rechazo
            
        Returns:
            dict: Resultado de la operación con mensaje y estado
        """
        try:
            # Verificar que quien rechaza es un administrador
            admin = User.get_by_id(admin_id)
            if not admin or admin.get('role') != UserManagementService.ROLE_ADMIN:
                return {
                    'success': False,
                    'message': 'Solo los administradores pueden rechazar empresas',
                    'status_code': 403
                }
            
            # Obtener la empresa
            company = Company.get_by_id(company_id)
            if not company:
                return {
                    'success': False,
                    'message': 'Empresa no encontrada',
                    'status_code': 404
                }
            
            # Actualizar estado a rechazado
            update_data = {
                'status': UserManagementService.STATUS_REJECTED
            }
            
            if reason:
                # Si el modelo Company tiene un campo para almacenar el motivo de rechazo
                update_data['rejection_reason'] = reason
                
            result = Company.update(company_id, update_data)
            
            if result:
                return {
                    'success': True,
                    'message': 'Empresa rechazada correctamente',
                    'status_code': 200
                }
            else:
                return {
                    'success': False,
                    'message': 'Error al rechazar la empresa',
                    'status_code': 500
                }
        except Exception as e:
            print(f"Error al rechazar empresa: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Autentica un usuario y verifica su estado de aprobación.
        Implementa RN01, RN02 y RN04.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            
        Returns:
            dict: Resultado de la operación con datos del usuario si es exitoso
        """
        try:
            # Intentar autenticar como usuario/admin
            user = User.authenticate(email, password)
            if user:
                # Si es administrador, permitir acceso directamente
                if user.get('role') == UserManagementService.ROLE_ADMIN:
                    return {
                        'success': True,
                        'message': 'Autenticación exitosa',
                        'user': user,
                        'user_type': 'admin',
                        'status_code': 200
                    }
                
                # Verificar estado del usuario (si no es admin)
                if user.get('status') != UserManagementService.STATUS_APPROVED:
                    return {
                        'success': False,
                        'message': 'Su cuenta está pendiente de aprobación por un administrador',
                        'status_code': 403
                    }
                
                return {
                    'success': True,
                    'message': 'Autenticación exitosa',
                    'user': user,
                    'user_type': 'user',
                    'status_code': 200
                }
            
            # Intentar autenticar como cliente
            client = Client.authenticate(email, password)
            if client:
                # Verificar si el cliente está aprobado (RN01)
                if client.get('status') != UserManagementService.STATUS_APPROVED:
                    return {
                        'success': False,
                        'message': 'Su cuenta de cliente está pendiente de aprobación por un administrador',
                        'status_code': 403
                    }
                
                return {
                    'success': True,
                    'message': 'Autenticación exitosa',
                    'user': client,
                    'user_type': 'client',
                    'status_code': 200
                }
            
            # Intentar autenticar como empresa
            company = Company.authenticate(email, password)
            if company:
                # Verificar si la empresa está aprobada (RN02)
                if company.get('status') != UserManagementService.STATUS_APPROVED:
                    return {
                        'success': False,
                        'message': 'Su cuenta de empresa está pendiente de validación por un administrador',
                        'status_code': 403
                    }
                
                return {
                    'success': True,
                    'message': 'Autenticación exitosa',
                    'user': company,
                    'user_type': 'company',
                    'status_code': 200
                }
            
            # Si llegamos aquí, las credenciales no son válidas
            return {
                'success': False,
                'message': 'Credenciales inválidas',
                'status_code': 401
            }
        except Exception as e:
            print(f"Error en autenticación: {str(e)}")
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def get_pending_clients():
        """
        Obtiene la lista de clientes pendientes de aprobación
        
        Returns:
            list: Lista de clientes pendientes
        """
        try:
            clients = Client.get_by_status(UserManagementService.STATUS_PENDING)
            return clients
        except:
            return []
    
    @staticmethod
    def get_pending_companies():
        """
        Obtiene la lista de empresas pendientes de aprobación
        
        Returns:
            list: Lista de empresas pendientes
        """
        try:
            companies = Company.get_by_status(UserManagementService.STATUS_PENDING)
            return companies
        except:
            return []