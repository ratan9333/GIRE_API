import jwt

def getUserFromHeader(token):
    token = str(token).replace('Bearer ', '')
    encoded_jwt = jwt.decode(token, "123456", algorithms=["HS256"])
    print(encoded_jwt)
    _user_id_ = encoded_jwt['sub']['user_id']
    # _user_type_ = encoded_jwt['sub']['user_type']
    return _user_id_

