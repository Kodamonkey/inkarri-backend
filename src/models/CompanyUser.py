import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables from .env file
load_dotenv()

class CompanyUser:
    def __init__(self, id=None, username=None, email=None, password=None, create_time=None, 
                 company_id=None, subscription=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.create_time = create_time
        self.company_id = company_id
        self.subscription = subscription

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
        conn = CompanyUser.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, create_time, company_id, subscription
                FROM company_users
            """)
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching company users: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = CompanyUser.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, create_time, company_id, subscription
                FROM company_users 
                WHERE id = %s
            """, (user_id,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error fetching company user: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_email(email):
        conn = CompanyUser.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM company_users WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error fetching company user by email: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_company_id(company_id):
        conn = CompanyUser.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, create_time, company_id, subscription
                FROM company_users 
                WHERE company_id = %s
            """, (company_id,))
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching company users by company_id: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def create(self):
        conn = CompanyUser.get_connection()
        cursor = conn.cursor()
        
        try:
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            
            # Set creation time to current time if not provided
            if not self.create_time:
                self.create_time = datetime.now()
                
            # Default subscription if not specified
            if not self.subscription:
                self.subscription = 'free'
            
            query = """
                INSERT INTO company_users (username, email, password, create_time, company_id, subscription) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.username, 
                self.email, 
                hashed_password, 
                self.create_time,
                self.company_id,
                self.subscription
            ))
            
            conn.commit()
            self.id = cursor.lastrowid
            return self.id
        except Exception as e:
            conn.rollback()
            print(f"Error creating company user: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(user_id, data):
        conn = CompanyUser.get_connection()
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
                elif key in ['username', 'email', 'company_id', 'subscription']:
                    set_values.append(f"{key} = %s")
                    params.append(value)
            
            if not set_values:
                return False
                
            query = f"UPDATE company_users SET {', '.join(set_values)} WHERE id = %s"
            params.append(user_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating company user: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete(user_id):
        conn = CompanyUser.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM company_users WHERE id = %s", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error deleting company user: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def authenticate(email, password):
        user = CompanyUser.get_by_email(email)
        if not user:
            return None
            
        # Check password
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user
        return None

    @staticmethod
    def update_subscription(user_id, new_subscription):
        """
        Update a user's subscription status
        
        Args:
            user_id: The user's ID
            new_subscription: The new subscription level (e.g., 'free', 'basic', 'premium')
        
        Returns:
            bool: True if successful, False otherwise
        """
        return CompanyUser.update(user_id, {'subscription': new_subscription})
    
    @staticmethod
    def get_by_subscription_type(subscription_type):
        """
        Get all users with a specific subscription type
        
        Args:
            subscription_type: The subscription type to filter by
        
        Returns:
            list: List of users with the specified subscription
        """
        conn = CompanyUser.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, create_time, company_id, subscription
                FROM company_users 
                WHERE subscription = %s
            """, (subscription_type,))
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching company users by subscription: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
            
    def to_dict(self):
        """
        Convert the CompanyUser object to a dictionary
        
        Returns:
            dict: Dictionary representation of the company user
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "create_time": self.create_time,
            "company_id": self.company_id,
            "subscription": self.subscription
        }