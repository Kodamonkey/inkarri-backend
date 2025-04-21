from models.Admin import Admin
from models.Client import Client
from models.Company import Company

class AdminManagementService:
    @staticmethod
    def approve_client_registration(admin_id, client_id):
        """
        RN01, RN03: Solo un administrador puede aprobar a un cliente. 
        """

        admin = Admin.get_by_id(admin_id)
        if not admin or admin['access'] != 'admin':
            raise PermissionError("Solo los administradores pueden aprobar registros de clientes")

        return Client.change_access(client_id, 'approved')

    @staticmethod
    def approve_company_registration(admin_id, company_id):
        """
        RN02, RN03: Solo un administrador puede aprobar una empresa para que pueda ofertar productos/servicios.
        """

        admin = Admin.get_by_id(admin_id)
        if not admin or admin['access'] != 'admin':
            raise PermissionError("Solo los administradores pueden aprobar registros de empresas")

        return Company.change_access(company_id, 'approved')

    @staticmethod
    def assign_Admin_role(admin_id, Admin_type, Admin_id, role):
        """
        RN04: Cada usuario tendrá un tipo de rol definido.
        """

        admin = Admin.get_by_id(admin_id)
        if not admin or admin['access'] != 'admin':
            raise PermissionError("Solo los administradores pueden cambiar el rol de un usuario")

        if Admin_type == 'client':
            return Client.change_access(Admin_id, role)
        elif Admin_type == 'company':
            return Company.change_access(Admin_id, role)
        elif Admin_type == 'admin':
            return Admin.update(Admin_id, {'access': role})
        else:
            raise ValueError("Tipo de usuario no reconocido")

    @staticmethod
    def get_Admin_permissions(Admin_id, Admin_type):
        """
        RN04: Retorna los permisos según el tipo de usuario.
        """

        if Admin_type == 'client':
            Admin = Client.get_by_id(Admin_id)
        elif Admin_type == 'company':
            Admin = Company.get_by_id(Admin_id)
        elif Admin_type == 'admin':
            Admin = Admin.get_by_id(Admin_id)
        else:
            raise ValueError("Tipo de usuario no reconocido")

        if not Admin:
            raise ValueError("Usuario no encontrado")

        return Admin['access']
