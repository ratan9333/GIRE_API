from helpers.misc.connection import *
from helpers.misc.helpers import *
from flask_jwt_extended import create_access_token

def socialUser(bodyData):
    if bodyData == None:
        return errorHandler("Missing Required Params")
    elif 'email' not in bodyData:
        return errorHandler("Missing Email")
    elif 'phone_number' not in bodyData:
        return errorHandler("Missing Phone Number")
    elif 'name' not in bodyData:
        return errorHandler("Missing Name")

    if True:
        query = "SELECT id_app_user FROM app_user WHERE email='"+str(bodyData['email'])+"' AND is_deleted = 0;"
        data = getServerData(query)
        if len(data) == 0:

            user_name = str(bodyData['name'])
            email = str(bodyData['email'])
            phone_number = str(bodyData['phone_number'])

            query = 'INSERT INTO app_user (email,phone_number,name,user_type) VALUES ("'+email+'","'+str(phone_number)+'","'+user_name+'","'+"SOCIAL"+'");'
            connection = engine.connect()
            connection.execute(query)
            connection.close()

            query = "SELECT id_app_user FROM app_user WHERE email='"+email+"'"
            data = getServerData(query)

            user_id = str(data['id_app_user'][0])

            token = create_access_token(identity={"email": email, "user_id": user_id})

            return getSignedJwt(token, str(bodyData['name']), str(user_id)), 200
        else:
            return errorHandler("Email already Exists")