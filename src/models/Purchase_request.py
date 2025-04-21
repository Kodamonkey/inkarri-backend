import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PurchaseRequest:
    def __init__(self, purchase_request_id=None, request_name=None, request_number=None, 
                 client_name=None, client_address=None, category=None, 
                 required_date=None, due_date=None):
        self.purchase_request_id = purchase_request_id
        self.request_name = request_name
        self.request_number = request_number
        self.client_name = client_name
        self.client_address = client_address
        self.category = category
        self.required_date = required_date
        self.due_date = due_date

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

    @staticmethod
    def get_all():
        conn = PurchaseRequest.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT purchase_request_id, request_name, request_number, client_name, 
                       client_address, category, required_date, due_date
                FROM purchase_requests
            """)
            requests = cursor.fetchall()
            return requests
        except Exception as e:
            print(f"Error fetching purchase requests: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(purchase_request_id):
        conn = PurchaseRequest.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT purchase_request_id, request_name, request_number, client_name, 
                       client_address, category, required_date, due_date
                FROM purchase_requests 
                WHERE purchase_request_id = %s
            """, (purchase_request_id,))
            purchase_request = cursor.fetchone()
            return purchase_request
        except Exception as e:
            print(f"Error fetching purchase request: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_request_number(request_number):
        conn = PurchaseRequest.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT purchase_request_id, request_name, request_number, client_name, 
                       client_address, category, required_date, due_date
                FROM purchase_requests 
                WHERE request_number = %s
            """, (request_number,))
            purchase_request = cursor.fetchone()
            return purchase_request
        except Exception as e:
            print(f"Error fetching purchase request by request number: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def create(self):
        conn = PurchaseRequest.get_connection()
        cursor = conn.cursor()
        
        try:
            # Default category if not specified
            if not self.category:
                self.category = 'servicio'  # Default category
            
            query = """
                INSERT INTO purchase_requests 
                (request_name, request_number, client_name, client_address, 
                 category, required_date, due_date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.request_name, 
                self.request_number, 
                self.client_name, 
                self.client_address,
                self.category,
                self.required_date,
                self.due_date
            ))
            
            conn.commit()
            self.purchase_request_id = cursor.lastrowid
            return self.purchase_request_id
        except Exception as e:
            conn.rollback()
            print(f"Error creating purchase request: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(purchase_request_id, data):
        conn = PurchaseRequest.get_connection()
        cursor = conn.cursor()
        
        try:
            # Build the update query dynamically based on provided data
            set_values = []
            params = []
            
            for key, value in data.items():
                if key in ['request_name', 'request_number', 'client_name', 
                          'client_address', 'category', 'required_date', 'due_date']:
                    set_values.append(f"{key} = %s")
                    params.append(value)
            
            if not set_values:
                return False
                
            query = f"UPDATE purchase_requests SET {', '.join(set_values)} WHERE purchase_request_id = %s"
            params.append(purchase_request_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating purchase request: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete(purchase_request_id):
        conn = PurchaseRequest.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM purchase_requests WHERE purchase_request_id = %s", (purchase_request_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error deleting purchase request: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_category(category):
        """
        Get all purchase requests with a specific category
        
        Args:
            category: The category to filter by
        
        Returns:
            list: List of purchase requests with the specified category
        """
        conn = PurchaseRequest.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT purchase_request_id, request_name, request_number, client_name, 
                       client_address, category, required_date, due_date 
                FROM purchase_requests 
                WHERE category = %s
            """, (category,))
            purchase_requests = cursor.fetchall()
            return purchase_requests
        except Exception as e:
            print(f"Error fetching purchase requests by category: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_client(client_name):
        """
        Get all purchase requests for a specific client
        
        Args:
            client_name: The client name to filter by
        
        Returns:
            list: List of purchase requests for the specified client
        """
        conn = PurchaseRequest.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT purchase_request_id, request_name, request_number, client_name, 
                       client_address, category, required_date, due_date 
                FROM purchase_requests 
                WHERE client_name LIKE %s
            """, (f"%{client_name}%",))
            purchase_requests = cursor.fetchall()
            return purchase_requests
        except Exception as e:
            print(f"Error fetching purchase requests by client: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_date_range(start_date, end_date):
        """
        Get all purchase requests within a date range
        
        Args:
            start_date: Start date for the range
            end_date: End date for the range
            
        Returns:
            list: List of purchase requests within the specified date range
        """
        conn = PurchaseRequest.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT purchase_request_id, request_name, request_number, client_name, 
                       client_address, category, required_date, due_date 
                FROM purchase_requests 
                WHERE required_date BETWEEN %s AND %s
            """, (start_date, end_date))
            purchase_requests = cursor.fetchall()
            return purchase_requests
        except Exception as e:
            print(f"Error fetching purchase requests by date range: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def to_dict(self):
        """
        Convert the PurchaseRequest object to a dictionary
        
        Returns:
            dict: Dictionary representation of the purchase request
        """
        return {
            "purchase_request_id": self.purchase_request_id,
            "request_name": self.request_name,
            "request_number": self.request_number,
            "client_name": self.client_name,
            "client_address": self.client_address,
            "category": self.category,
            "required_date": self.required_date,
            "due_date": self.due_date
        }