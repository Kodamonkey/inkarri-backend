from decouple import config
import pymysql


def get_connection():
    try:
        return pymysql.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),  
            db=config('MYSQL_DATABASE')
        )
    except pymysql.MySQLError as ex:
        print(f"Error connecting to MySQL: {ex}")
        return None