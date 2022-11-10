from sys import api_version
from helpers.misc.connection import *
from helpers.misc.helpers import *
from flask_jwt_extended import create_access_token


def createUser(bodyData, user_type):
    if bodyData == None:
        return errorHandler("Missing Required Params")
    elif 'email' not in bodyData:
        return errorHandler("Missing Email")
    elif 'password' not in bodyData:
        return errorHandler("Missing Password")
    elif 'name' not in bodyData:
        return errorHandler("Missing Name")



    if user_type == 'civilian':
        query = f"SELECT id_app_user FROM app_user WHERE email='" + \
            str(bodyData['email'])+"' AND is_deleted = 0;"
        civ_users = getServerData(query)
        if len(civ_users) != 0:
            return errorHandler("Email already Exists")

    if user_type == 'department':
        query = f"SELECT id_app_user FROM dep_app_user WHERE email='" + \
            str(bodyData['email'])+"' AND is_deleted = 0;"
        dep_users = getServerData(query)
        if len(dep_users) != 0:
            return errorHandler("Email already Exists")

    user_name = str(bodyData['name'])
    email = str(bodyData['email'])
    if "m_department" in bodyData:
        m_department = str(bodyData['m_department'])
    else:
        m_department = None

    if "m_designation" in bodyData:
        m_designation = str(bodyData['m_designation'])
    else:
        m_designation = None

    if "m_user_type" in bodyData:
        m_user_type = str(bodyData['m_user_type'])
    else:
        m_user_type = None

    if 'phone_number' in bodyData:
        phone_number = str(bodyData['phone_number'])
    else:
        phone_number = None

    user_pwd = passwordHasher(bodyData['password'])
    user_pwd = user_pwd.decode('utf-8')

    if user_type == 'civilian':
        tname = 'app_user'
    else:
        tname = 'dep_app_user'


    query = f'INSERT INTO {tname} (email,password,name,user_type,phone_number,m_designation_id,m_department_id,m_user_type_id) VALUES ("' + \
        email+'","'+str(user_pwd)+'","'+user_name+'","' + \
        "APP"+'","'+str(phone_number)+'","'+str(m_designation)+'","'+str(m_department)+'","'+str(m_user_type)+'");'

    connection = engine.connect()
    connection.execute(query)
    connection.close()

    query = f"SELECT id_app_user,email,photo_url,phone_number FROM {tname} WHERE email='"+email+"'"
    data = getServerData(query)

    user_id = str(data['id_app_user'][0])
    email = str(data['email'][0])
    phone_number = str(data['phone_number'][0])
    photo_url = str(data['photo_url'][0])

    token = create_access_token(identity={"email": email, "user_id": user_id})

    if user_type == 'civilian':
        return getSignedJwt(token, str(bodyData['name'],), int(user_id), email, photo_url, phone_number), 200
    else:
        return {
            "meta": {
                "error": 0,
                "code": 200,
                "msg": "Success",
                "data": {}
            }
        }
