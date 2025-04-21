from models.Company import Company
from models.Purchase_request import PurchaseRequest
from models.Client import Client

class QuotationService:
    @staticmethod
    def get_companies_for_request_category(request_category):
        """
        RN05: Retorna empresas registradas en la categoría de la solicitud.
        """
        return Company.get_by_categories(request_category)

    @staticmethod
    def send_request_to_companies(client_id, purchase_request_data):
        """
        RN06: Enviar solicitud a múltiples empresas dentro de la misma categoría.
        """

        client = Client.get_by_id(client_id)
        if not client:
            raise ValueError("Cliente no válido")

        # Crear la solicitud de cotización
        pr = PurchaseRequest(**purchase_request_data)
        request_id = pr.create()

        # Obtener empresas de la categoría
        companies = Company.get_by_categories(pr.category)

        return {
            "request_id": request_id,
            "notified_companies": [c['id'] for c in companies]
        }

    @staticmethod
    def validate_quotation_visibility(company_id, request_id):
        """
        RN07: Validar que una empresa no pueda ver cotizaciones de otras empresas.
        Este método simplemente verifica si la empresa puede acceder a una solicitud específica.
        """

        company = Company.get_by_id(company_id)
        if not company:
            raise ValueError("Empresa no encontrada")

        request = PurchaseRequest.get_by_id(request_id)
        if not request:
            raise ValueError("Solicitud de cotización no encontrada")

        if company['categories_id'] != request['category']:
            raise PermissionError("Acceso denegado a esta cotización")

        return True

    @staticmethod
    def validate_quotation_fields(quotation):
        """
        RN08: Validar que una cotización tenga descripción, precio estimado y tiempo de entrega.
        """
        required_fields = ['description', 'estimated_price', 'delivery_time']
        missing = [field for field in required_fields if not quotation.get(field)]

        if missing:
            raise ValueError(f"Faltan campos requeridos en la cotización: {', '.join(missing)}")

        return True