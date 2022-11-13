from functools import wraps
from flask import request
from .models import User, JWTTokenBlocklist
from .config import BaseConfig
import jwt

class TokenReq():
    def token_reuired(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = None

            if "authorization" in request.headers:
                token = request.headers["authorization"]

            if not token:
                return {"success": False, "msg": "valid token not found"}, 400
            
            try: 
                data = jwt.decode(token,BaseConfig.SECRET_KEY, alorithms=["HS256"])
                current_user = User.get_by_email(data["email"])

                if not current user:
                    return {
                        "success":False,
                        "msg": "User doesn't exist."
                    },400

                token_exp = db.session.query(JWTTokenBlocklist.id).filter_by(
                    jwt_token=token
                ).scaler()

                if not current_user.check_jwt_auth_active():
                    return{
                        "success": False,
                        "msg": "Expired Token"},400
            
            except:
                return{
                    "success": False,
                    "msg": "Invalid Token"
                },400
            
            return f(current_user, *args, **kwargs)
        
        return decorator
