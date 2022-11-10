from helpers.misc.helpers import *
from helpers.misc.connection import *
from flask_jwt_extended import create_access_token

def getUserPass(email,user_type):
    if user_type == 'civilian':
        try:
            query = "SELECT email,password,id_app_user,name FROM app_user WHERE email = '"+str(email)+"';"
            user_data = getServerData(query)
            return user_data['password'][0],user_data['id_app_user'][0],user_data['name'][0],'civilian'
        except:
            return None,None,None,None
    elif user_type == 'department':
        try:
            query = "SELECT email,password,id_app_user,name FROM app_user WHERE email = '"+str(email)+"';"
            user_data = getServerData(query)
            return user_data['password'][0],user_data['id_app_user'][0],user_data['name'][0],'department'
        except:
            return None,None,None,None

def userLogin(bodyData,user_type):
    if 'email' not in bodyData:
        return errorHandler("Email is required")
    elif 'password' not in bodyData:
        return errorHandler("Password is required")

    _email_ = str(bodyData["email"])
    _password_ = str(bodyData["password"])

    server_password,user_id,user_name,user_type = getUserPass(_email_,user_type)

    if server_password != None:
        if bcrypt.checkpw(bytes(_password_, 'utf-8'), bytes(server_password, 'utf-8')):
            token = create_access_token(identity={"email": _email_, "user_id": str(user_id),'user_type':user_type})
            return getSignedJwt(token, user_name, str(user_id)), 200
        else:
            return errorHandler('Password Incorrect')
    else:
        return errorHandler("Email dosen't Exist")