from helpers.misc.helpers import *
from helpers.misc.connection import *
from flask_jwt_extended import create_access_token


def getUserPass(email, user_type):
    if user_type == 'civilian':
        try:
            query = "SELECT email,password,id_app_user,name,phone_number,photo_url FROM app_user WHERE is_deleted = 0 AND email = '" + \
                str(email)+"';"
            user_data = getServerData(query)
            return user_data['password'][0], user_data['id_app_user'][0], user_data['name'][0], 'civilian', user_data['email'][0], user_data['photo_url'][0], user_data['phone_number'][0],None,None,None
        except:
            return None, None, None, None, None, None, None,None, None, None
    elif user_type == 'department':
        try:
            query = "SELECT email,password,id_app_user,name,phone_number,photo_url,m_designation_id,m_department_id,m_user_type_id FROM dep_app_user WHERE is_deleted = 0 AND email = '" + \
                str(email)+"';"
            print(query)
            user_data = getServerData(query)
            return user_data['password'][0], user_data['id_app_user'][0], user_data['name'][0], 'department', user_data['email'][0], user_data['photo_url'][0], user_data['phone_number'][0],int(user_data['m_designation_id'][0]),int(user_data['m_department_id'][0]),int(user_data['m_user_type_id'][0])
        except:
            return None, None, None, None, None, None, None, None, None,None


def userLogin(bodyData, user_type):
    if 'email' not in bodyData:
        return errorHandler("Email is required")
    elif 'password' not in bodyData:
        return errorHandler("Password is required")

    _email_ = str(bodyData["email"])
    _password_ = str(bodyData["password"])

    server_password, user_id, user_name, user_type, email, photo_url, phone_number,m_designation,m_department,m_user_type = getUserPass(
        _email_, user_type)

    if server_password != None:
        if bcrypt.checkpw(bytes(_password_, 'utf-8'), bytes(server_password, 'utf-8')):
            token = create_access_token(
                identity={"email": _email_, "user_id": str(user_id), 'user_type': user_type})
            return getSignedJwt(token, user_name, str(user_id), email, photo_url, phone_number,m_designation,m_department,m_user_type), 200
        else:
            return errorHandler('Password Incorrect')
    else:
        return errorHandler("Email dosen't Exist")
