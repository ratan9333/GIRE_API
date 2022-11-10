from helpers.misc.connection import *
from helpers.misc.helpers import *
from flask_jwt_extended import create_access_token

def createUser(bodyData,user_type):
    if bodyData == None:
        return errorHandler("Missing Required Params")
    elif 'email' not in bodyData:
        return errorHandler("Missing Email")
    elif 'password' not in bodyData:
        return errorHandler("Missing Password")
    elif 'name' not in bodyData:
        return errorHandler("Missing Name")

    if user_type == 'civilian':
        query = f"SELECT id_app_user FROM app_user WHERE email='"+str(bodyData['email'])+"' AND is_deleted = 0;"
        civ_users = getServerData(query)
        if len(civ_users) != 0:
            return errorHandler("Email already Exists")

    if user_type == 'department':
        query = f"SELECT id_app_user FROM app_user WHERE email='"+str(bodyData['email'])+"' AND is_deleted = 0;"
        dep_users = getServerData(query)
        if len(dep_users) != 0:
            return errorHandler("Email already Exists")
        
    user_name = str(bodyData['name'])
    email = str(bodyData['email'])

    user_pwd = passwordHasher(bodyData['password'])
    user_pwd = user_pwd.decode('utf-8')
    
    if user_type == 'civilian':
        tname = 'app_user'
    else:
        tname = 'app_user'

    query = f'INSERT INTO {tname} (email,password,name,user_type) VALUES ("'+email+'","'+str(user_pwd)+'","'+user_name+'","'+"APP"+'");'

    connection = engine.connect()
    connection.execute(query)
    connection.close()

    query = f"SELECT id_app_user FROM {tname} WHERE email='"+email+"'"
    data = getServerData(query)

    user_id = str(data['id_app_user'][0])

    token = create_access_token(identity={"email": email, "user_id": user_id})

    return getSignedJwt(token, str(bodyData['name']), str(user_id)), 200