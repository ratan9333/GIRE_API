import bcrypt
import ast

def errorHandler(message):
    error = {
        "meta": {
            "error": 1,
            "code": 400,
            "msg": message,
            "data": {}      
            }
        }
    return error, 400

def getSignedJwt(_token_, username, user_id,email,photo_url,phone_number,m_designation,m_department,m_user_type):
    data = {
        "meta": {
            "error": 0,
            "code": 200,
            "msg": "Success",
            "data": {"access_token": _token_, "user_name": str(username), "user_id": str(user_id),"email":email,"photo_url":photo_url,"phone_number":phone_number,
                        "m_designation":m_designation,"m_department":m_department,"m_user_type":m_user_type}
        }
    }
    return data

def responseWrapper(_json_):
    data = {
        "meta": {
            "error": 0,
            "code": 200,
            "msg": "success",
            "data": _json_
        }
    }
    return data

def passwordHasher(passwd):
    passwd = bytes(str(passwd), 'utf-8')
    hashed_passwd = bcrypt.hashpw(passwd, bcrypt.gensalt(10))
    return hashed_passwd

def _dataframeToJson_(data):
    data.reset_index(inplace=True,drop=True)
    data = data.loc[:,~data.columns.duplicated()].copy()
    columns_ = list(data.columns)
    dataJson = []
    for i in range(len(data)):
        tempJson = {}
        for each_column in columns_:
            try:
                data[each_column][i] = ast.literal_eval(data[each_column][i])
            except:pass
            if isinstance(data[each_column][i], list):
                tempJson[each_column] = data[each_column][i]
            else:
                if str(data[each_column][i]) in ["None","nan"]:
                    tempJson[each_column] = None
                else:
                    try:
                        tempJson[each_column] = int(data[each_column][i])
                    except:
                        tempJson[each_column] = str(data[each_column][i])
        dataJson.append(tempJson)
    return dataJson