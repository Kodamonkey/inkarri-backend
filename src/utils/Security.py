# Generation Token
import datetime
import pytz
from decouple import config
import jwt

class Security:
    secret = config('JWT_KEY')
    tz = pytz.timezone('America/Santiago')
    
    @classmethod
    def generate_token(cls, authenticated_user):
        """
        Generate a JWT token with the given data.
        """
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10),
            'username': authenticated_user.username,
            'email': authenticated_user.full_name,
            'roles': ['Administrator']
        }
        return jwt.encode(payload, cls.secret, algorithm='HS256')  
    
    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' not in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(' ')[1]
            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=['HS256'])
                    roles = list(payload['roles'])
                    
                    if 'Administrator' in roles:
                        return True
                    return False
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                    return False
        return False

         