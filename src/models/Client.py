import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables from .env file
load_dotenv()

class Client:
    def __init__(self, id=None, username=None, email=None, password=None, 
                 create_time=None, access=None, subscription=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.create_time = create_time
        self.access = access
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
        conn = Client.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, create_time, access, subscription
                FROM clients
            """)
            clients = cursor.fetchall()
            return clients
        except Exception as e:
            print(f"Error fetching clients: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(client_id):
        conn = Client.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, create_time, access, subscription
                FROM clients 
                WHERE id = %s
            """, (client_id,))
            client = cursor.fetchone()
            return client
        except Exception as e:
            print(f"Error fetching client: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_email(email):
        conn = Client.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM clients WHERE email = %s", (email,))
            client = cursor.fetchone()
            return client
        except Exception as e:
            print(f"Error fetching client by email: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_username(username):
        conn = Client.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM clients WHERE username = %s", (username,))
            client = cursor.fetchone()
            return client
        except Exception as e:
            print(f"Error fetching client by username: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def create(self):
        conn = Client.get_connection()
        cursor = conn.cursor()
        
        try:
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            
            # Set creation time to current time if not provided
            if not self.create_time:
                self.create_time = datetime.now()
                
            # Default access level if not specified
            if not self.access:
                self.access = 'client'  # Default access level
                
            # Default subscription if not specified
            if not self.subscription:
                self.subscription = 'free'  # Default subscription
            
            query = """
                INSERT INTO clients (username, email, password, create_time, access, subscription) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.username, 
                self.email, 
                hashed_password, 
                self.create_time,
                self.access,
                self.subscription
            ))
            
            conn.commit()
            self.id = cursor.lastrowid
            return self.id
        except Exception as e:
            conn.rollback()
            print(f"Error creating client: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(client_id, data):
        conn = Client.get_connection()
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
                elif key in ['username', 'email', 'access', 'subscription']:
                    set_values.append(f"{key} = %s")
                    params.append(value)
            
            if not set_values:
                return False
                
            query = f"UPDATE clients SET {', '.join(set_values)} WHERE id = %s"
            params.append(client_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating client: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete(client_id):
        conn = Client.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM clients WHERE id = %s", (client_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error deleting client: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def authenticate(email, password):
        client = Client.get_by_email(email)
        if not client:
            return None
            
        # Check password
        if bcrypt.checkpw(password.encode('utf-8'), client['password'].encode('utf-8')):
            return client
        return None
    
    @staticmethod
    def update_subscription(client_id, new_subscription):
        """
        Update a client's subscription
        
        Args:
            client_id: The client's ID
            new_subscription: The new subscription level
        
        Returns:
            bool: True if successful, False otherwise
        """
        return Client.update(client_id, {'subscription': new_subscription})
    
    @staticmethod
    def change_access(client_id, new_access):
        """
        Change a client's access level
        
        Args:
            client_id: The client's ID
            new_access: The new access level
        
        Returns:
            bool: True if successful, False otherwise
        """
        return Client.update(client_id, {'access': new_access})
    
    @staticmethod
    def get_by_subscription(subscription_type):
        """
        Get all clients with a specific subscription type
        
        Args:
            subscription_type: The subscription type to filter by
        
        Returns:
            list: List of clients with the specified subscription
        """
        conn = Client.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, create_time, access, subscription
                FROM clients 
                WHERE subscription = %s
            """, (subscription_type,))
            clients = cursor.fetchall()
            return clients
        except Exception as e:
            print(f"Error fetching clients by subscription: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_recent_clients(limit=10):
        """
        Get the most recently created clients
        
        Args:
            limit: Maximum number of clients to return
            
        Returns:
            list: List of recently created clients
        """
        conn = Client.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT id, username, email, create_time, access, subscription
                FROM clients 
                ORDER BY create_time DESC
                LIMIT %s
            """, (limit,))
            clients = cursor.fetchall()
            return clients
        except Exception as e:
            print(f"Error fetching recent clients: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def to_dict(self):
        """
        Convert the Client object to a dictionary
        
        Returns:
            dict: Dictionary representation of the client
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "create_time": self.create_time,
            "access": self.access,
            "subscription": self.subscription
        }