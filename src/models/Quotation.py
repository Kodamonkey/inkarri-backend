class Quotation:
    def __init__(self, quotation_id=None, company_id=None, request_id=None,
                 description=None, estimated_price=None, delivery_time=None, created_at=None):
        self.quotation_id = quotation_id
        self.company_id = company_id
        self.request_id = request_id
        self.description = description
        self.estimated_price = estimated_price
        self.delivery_time = delivery_time
        self.created_at = created_at

    @staticmethod
    def get_connection():
        import mysql.connector, os
        from dotenv import load_dotenv
        load_dotenv()
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

    def create(self):
        conn = Quotation.get_connection()
        cursor = conn.cursor()
        from datetime import datetime

        try:
            if not self.created_at:
                self.created_at = datetime.now()

            query = """
                INSERT INTO quotations (company_id, request_id, description, estimated_price, delivery_time, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.company_id,
                self.request_id,
                self.description,
                self.estimated_price,
                self.delivery_time,
                self.created_at
            ))
            conn.commit()
            self.quotation_id = cursor.lastrowid
            return self.quotation_id
        except Exception as e:
            conn.rollback()
            print(f"Error creating quotation: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_request_id(request_id):
        conn = Quotation.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT quotation_id, company_id, request_id, description, estimated_price, delivery_time, created_at
                FROM quotations WHERE request_id = %s
            """, (request_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching quotations: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    def to_dict(self):
        return {
            "quotation_id": self.quotation_id,
            "company_id": self.company_id,
            "request_id": self.request_id,
            "description": self.description,
            "estimated_price": self.estimated_price,
            "delivery_time": self.delivery_time,
            "created_at": self.created_at
        }