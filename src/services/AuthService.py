from src.database.db_mysql import get_connection
from src.models.User import User

class AuthService():
    @classmethod
    def login_user(cls, user):
        try: 
            connection = get_connection()
            print(f"conexion db: {connection}")
            authenticated_user = None
            
            with connection.cursor() as cursor:
                cursor.execute("call sp_verifyIdentity(%s, %s)", (user.username, user.password))
                row = cursor.fetchone()
                
                if row != None:
                    authenticated_user = User(int(row[0]), row[1], None, row[2])
                
                connection.close()
                return authenticated_user
            
        except Exception as ex:
            print(f"Error connecting to MySQL: {ex}")
            return None