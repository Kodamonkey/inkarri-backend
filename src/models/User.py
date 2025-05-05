import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables from .env file
load_dotenv()

class User:
    def __init__(self, user_id=None, name=None, email=None, rut=None, password=None, role=None, 
                 status=None, created_at=None, updated_at=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.rut = rut
        self.password = password
        self.role = role
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

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
            cursor.execute("""
                SELECT user_id, name, email, rut, role, status, created_at, updated_at 
                FROM users
            """)
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
            cursor.execute("""
                SELECT user_id, name, email, rut, role, status, created_at, updated_at 
                FROM users 
                WHERE user_id = %s
            """, (user_id,))
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
            
            # Set timestamps if not provided
            current_time = datetime.now()
            if not self.created_at:
                self.created_at = current_time
            if not self.updated_at:
                self.updated_at = current_time
                
            # Default role if not specified
            if not self.role:
                self.role = 'user'  # Default role
            
            # Default status if not specified
            if not self.status:
                self.status = 'active'  # Default status
            
            query = """
                INSERT INTO users (name, email, rut, password, role, status, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.name, 
                self.email, 
                self.rut,
                hashed_password, 
                self.role,
                self.status,
                self.created_at,
                self.updated_at
            ))
            
            conn.commit()
            self.user_id = cursor.lastrowid
            return self.user_id
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
            # Always update the updated_at timestamp
            data['updated_at'] = datetime.now()
            
            # Build the update query dynamically based on provided data
            set_values = []
            params = []
            
            for key, value in data.items():
                if key == 'password' and value:
                    # Hash password if it's being updated
                    hashed_password = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
                    set_values.append(f"{key} = %s")
                    params.append(hashed_password)
                elif key in ['name', 'email', 'role', 'status', 'updated_at']:
                    set_values.append(f"{key} = %s")
                    params.append(value)
            
            if not set_values:
                return False
                
            query = f"UPDATE users SET {', '.join(set_values)} WHERE user_id = %s"
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
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
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
            # Check if user is active
            if user['status'] != 'active':
                return None
            return user
        return None

    @staticmethod
    def change_status(user_id, new_status):
        """
        Change a user's status (active, inactive, suspended, etc.)
        
        Args:
            user_id: The user's ID
            new_status: The new status value
        
        Returns:
            bool: True if successful, False otherwise
        """
        return User.update(user_id, {'status': new_status})
        
    @staticmethod
    def change_role(user_id, new_role):
        """
        Change a user's role
        
        Args:
            user_id: The user's ID
            new_role: The new role value
        
        Returns:
            bool: True if successful, False otherwise
        """
        return User.update(user_id, {'role': new_role})
        
    @staticmethod
    def get_by_role(role):
        """
        Get all users with a specific role
        
        Args:
            role: The role to filter by
        
        Returns:
            list: List of users with the specified role
        """
        conn = User.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT user_id, name, email, role, status, created_at, updated_at 
                FROM users 
                WHERE role = %s
            """, (role,))
            users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching users by role: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()