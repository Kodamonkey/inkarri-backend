import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables from .env file
load_dotenv()

class Company:
    def __init__(self, id=None, username=None, email=None, password=None, 
                 access=None, categories_id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.access = access
        self.categories_id = categories_id

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
        conn = Company.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, access, categories_id
                FROM companies
            """)
            companies = cursor.fetchall()
            return companies
        except Exception as e:
            print(f"Error fetching companies: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(company_id):
        conn = Company.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, access, categories_id
                FROM companies 
                WHERE id = %s
            """, (company_id,))
            company = cursor.fetchone()
            return company
        except Exception as e:
            print(f"Error fetching company: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_email(email):
        conn = Company.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM companies WHERE email = %s", (email,))
            company = cursor.fetchone()
            return company
        except Exception as e:
            print(f"Error fetching company by email: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_categories(categories_id):
        conn = Company.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, access, categories_id
                FROM companies 
                WHERE categories_id = %s
            """, (categories_id,))
            companies = cursor.fetchall()
            return companies
        except Exception as e:
            print(f"Error fetching companies by category: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def create(self):
        conn = Company.get_connection()
        cursor = conn.cursor()
        
        try:
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
                
            # Default access level if not specified
            if not self.access:
                self.access = 'company'  # Default access level
            
            query = """
                INSERT INTO companies (username, email, password, access, categories_id) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.username, 
                self.email, 
                hashed_password, 
                self.access,
                self.categories_id
            ))
            
            conn.commit()
            self.id = cursor.lastrowid
            return self.id
        except Exception as e:
            conn.rollback()
            print(f"Error creating company: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(company_id, data):
        conn = Company.get_connection()
        cursor = conn.cursor()
        
        try:
            # Build the update query dynamically based on provided data
            set_values = []
            params = []
            
            for key, value in data.items():
                if key == 'password' and value:
                    # Hash password if it's being updated
                    hashed_password = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
                    set_values.append(f"{key} = %s")
                    params.append(hashed_password)
                elif key in ['username', 'email', 'access', 'categories_id']:
                    set_values.append(f"{key} = %s")
                    params.append(value)
            
            if not set_values:
                return False
                
            query = f"UPDATE companies SET {', '.join(set_values)} WHERE id = %s"
            params.append(company_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating company: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete(company_id):
        conn = Company.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM companies WHERE id = %s", (company_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error deleting company: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def authenticate(email, password):
        company = Company.get_by_email(email)
        if not company:
            return None
            
        # Check password
        if bcrypt.checkpw(password.encode('utf-8'), company['password'].encode('utf-8')):
            return company
        return None
    
    @staticmethod
    def change_access(company_id, new_access):
        """
        Change a company's access level
        
        Args:
            company_id: The company's ID
            new_access: The new access level
        
        Returns:
            bool: True if successful, False otherwise
        """
        return Company.update(company_id, {'access': new_access})
    
    @staticmethod
    def change_category(company_id, new_categories_id):
        """
        Change a company's category
        
        Args:
            company_id: The company's ID
            new_categories_id: The new category ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        return Company.update(company_id, {'categories_id': new_categories_id})
    
    def to_dict(self):
        """
        Convert the Company object to a dictionary
        
        Returns:
            dict: Dictionary representation of the company
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "access": self.access,
            "categories_id": self.categories_id
        }