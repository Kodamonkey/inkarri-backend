import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables from .env file
load_dotenv()

class Admin:
    def __init__(self, id=None, Adminname=None, email=None, password=None, create_time=None, access=None):
        self.id = id
        self.Adminname = Adminname
        self.email = email
        self.password = password
        self.create_time = create_time
        self.access = access

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            Admin=os.getenv('DB_Admin'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

    @staticmethod
    def get_all():
        conn = Admin.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, Adminname, email, create_time, access FROM Admins")
            Admins = cursor.fetchall()
            return Admins
        except Exception as e:
            print(f"Error fetching Admins: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(Admin_id):
        conn = Admin.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, Adminname, email, create_time, access FROM Admins WHERE id = %s", (Admin_id,))
            Admin = cursor.fetchone()
            return Admin
        except Exception as e:
            print(f"Error fetching Admin: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_email(email):
        conn = Admin.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM Admins WHERE email = %s", (email,))
            Admin = cursor.fetchone()
            return Admin
        except Exception as e:
            print(f"Error fetching Admin by email: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def create(self):
        conn = Admin.get_connection()
        cursor = conn.cursor()
        
        try:
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            
            # Set creation time to current time if not provided
            if not self.create_time:
                self.create_time = datetime.now()
                
            # Default access level if not specified
            if not self.access:
                self.access = 'Admin'  # Default to regular Admin
            
            query = """INSERT INTO Admins (Adminname, email, password, create_time, access) 
                    VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                self.Adminname, 
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
            print(f"Error creating Admin: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update(Admin_id, data):
        conn = Admin.get_connection()
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
                elif key in ['Adminname', 'email', 'access']:
                    set_values.append(f"{key} = %s")
                    params.append(value)
            
            if not set_values:
                return False
                
            query = f"UPDATE Admins SET {', '.join(set_values)} WHERE id = %s"
            params.append(Admin_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating Admin: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def delete(Admin_id):
        conn = Admin.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM Admins WHERE id = %s", (Admin_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error deleting Admin: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def authenticate(email, password):
        Admin = Admin.get_by_email(email)
        if not Admin:
            return None
            
        # Check password
        if bcrypt.checkpw(password.encode('utf-8'), Admin['password'].encode('utf-8')):
            return Admin
        return None