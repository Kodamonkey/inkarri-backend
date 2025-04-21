import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables from .env file
load_dotenv()

class User:
    def __init__(self, id=None, username=None, email=None, password=None, create_time=None, access=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.create_time = create_time
        self.access = access

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
        conn = User.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, username, email, create_time, access FROM users")
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching users: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = User.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, username, email, create_time, access FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error fetching user: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_email(email):
        conn = User.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error fetching user by email: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def create(self):
        conn = User.get_connection()
        cursor = conn.cursor()
        
        try:
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            
            # Set creation time to current time if not provided
            if not self.create_time:
                self.create_time = datetime.now()
                
            # Default access level if not specified
            if not self.access:
                self.access = 'user'  # Default to regular user
            
            query = """INSERT INTO users (username, email, password, create_time, access) 
                    VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                self.username, 
                self.email, 
                hashed_password, 
                self.create_time,
                self.access
            ))
            
            conn.commit()
            self.id = cursor.lastrowid
            return self.id
        except Exception as e:
            conn.rollback()
            print(f"Error creating user: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(user_id, data):
        conn = User.get_connection()
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
                elif key in ['username', 'email', 'access']:
                    set_values.append(f"{key} = %s")
                    params.append(value)
            
            if not set_values:
                return False
                
            query = f"UPDATE users SET {', '.join(set_values)} WHERE id = %s"
            params.append(user_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating user: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete(user_id):
        conn = User.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error deleting user: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def authenticate(email, password):
        user = User.get_by_email(email)
        if not user:
            return None
            
        # Check password
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user
        return None