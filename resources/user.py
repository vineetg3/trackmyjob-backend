from flask_restful import Resource, reqparse
from models.users import UserModel
from models.tokenBlacklist import TokenBlocklist
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt
from datetime import datetime
import datetime
from dateTimeHelper import get_current_IST_dt
from .utilities import printResponse

class UserRegister(Resource):
    parser = reqparse.RequestParser() 
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return printResponse({"message": "A user with that email already exists"}, 400)
        print(data)
        user = UserModel(**data)
        user.hash_password()
        user.save_to_db()

        return printResponse({"message": "User created successfully.","id":user._id}, 201)


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserLogin.parser.parse_args()
        
        user = UserModel.find_by_email(data['email'])

        if user==None:
            return printResponse({"message": "User doesnt exsist"}, 400)
        
        authorized =user.check_password(data['password'])
        if not authorized:
            return printResponse({"message": "Email or password incorrect"}, 401)

        expires = datetime.timedelta(hours=2)
        access_token = create_access_token(identity=str(user._id), expires_delta=expires)
        return printResponse({
            "message": "verified",
            "id":user._id,
            "username":user.username,
            "email":user.email,
            "access_token":access_token,  
        }, 200)

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        jti = get_jwt()["jti"]
        token = TokenBlocklist(jti=jti, created_at=get_current_IST_dt())
        token.save_to_db()
        return printResponse({"message":"JWT revoked","user_id":user_id})

        
