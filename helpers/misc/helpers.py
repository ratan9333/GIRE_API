import bcrypt

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

def getSignedJwt(_token_, username, user_id):
    data = {
        "meta": {
            "error": 0,
            "code": 200,
            "msg": "Success",
            "data": {"token": _token_, "user_name": str(username), "user_id": user_id}
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
            # print(data[each_column])
            if isinstance(data[each_column][i], list):
                tempJson[each_column] = data[each_column][i]
            else:
                tempJson[each_column] = str(data[each_column][i])
        dataJson.append(tempJson)
    return dataJson