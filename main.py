from flask import Flask, request
from flask_jwt_extended import create_access_token,jwt_required,JWTManager
from helpers.misc.helpers import *
from helpers.misc.connection import *
from helpers.misc.decodeToken import getUserFromHeader
from helpers.misc.helpers import _dataframeToJson_
from helpers.master_data.master_data import masterData
from helpers.signup.social_user import socialUser
from helpers.upload_data.upload_data import sqlUpload, sqlUploadDataQuery
from helpers.login.user_login import *
from helpers.signup.create_user import *
from datetime import timedelta
from waitress import serve
import os

from helpers.upload_data.upload_survey import uploadSurveyData

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = '123456'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1440)
jwt = JWTManager(app)

#login
@app.route('/<user_type>/login', methods=['POST'])
def login(user_type):
    if user_type not in ['department','civilian']:
        return errorHandler('Invalid URL')
    try:
        bodyData = request.get_json()
        if bodyData == None:
            return errorHandler('Missing Required Params')
    except:
        return errorHandler('Missing Data')
    return userLogin(bodyData,user_type)

#create user
@app.route('/<user_type>/signup', methods=['POST'])
def User(user_type):
    if user_type not in ['department','civilian','social']:
        return errorHandler('Invalid URL')
    if request.method == 'POST':
        bodyData = request.get_json()
        if user_type in  ['department','civilian']:
            return createUser(bodyData,user_type)
        else:
            return socialUser(bodyData)

#upload data
@app.route('/<user_type>/submit_data/<data_type>', methods=['POST'])
@jwt_required()
def uploadData(user_type,data_type):
    if user_type not in ['department','civilian']:
        return errorHandler('Invalid URL')

    bodyData = request.get_json()
    user_id = getUserFromHeader(request.headers['authorization'])

    if data_type == 'other':
        data = sqlUpload(bodyData,user_id,user_type)
        return responseWrapper(data)
    if data_type == 'survey':
        if user_type not in ['department']:
            return errorHandler('Invalid URL')
        return uploadSurveyData(bodyData,user_id,user_type)

#upload documents
@app.route('/<user_type>/upload_documents', methods=['POST'])
@jwt_required()
def uploadDocuments(user_type):
    if user_type not in ['department','civilian']:
        return errorHandler('Invalid URL')

    try:
        file = request.files['document']
        token = request.headers['authorization']
        user_id = getUserFromHeader(token)

        file_name = str(file.filename)

        if user_type == 'civilian':
            doc_path = 'documents/civilian'
        else:
            doc_path = 'documents/department'
        
        document_folders = os.listdir(doc_path)
        if file_name in document_folders:
            return errorHandler("File Name already exists")
            # os.mkdir(doc_path+'/'+str(user_id))

        file.save(doc_path+'/'+file_name)

        return {"msg":"document uploaded successfully"}
    except Exception as e:
        return errorHandler('failed to upload document. Error: '+str(e))

#upload Pictures
@app.route('/<user_type>/upload_image', methods=['POST'])
@jwt_required()
def uploadPictures(user_type):
    if user_type not in ['department','civilian']:
        return errorHandler('Invalid URL')

    try:
        file = request.files['image']
        token = request.headers['authorization']
        user_id = getUserFromHeader(token)

        file_name = str(file.filename)

        if user_type == 'civilian':
            doc_path = 'images/civilian'
        else:
            doc_path = 'images/department'
        
        document_folders = os.listdir(doc_path)
        if file_name in document_folders:
            return errorHandler("Image Name already exists")
            # os.mkdir(doc_path+'/'+str(user_id))

        file.save(doc_path+'/'+file_name)

        return {"msg":"Image uploaded successfully"}
    except Exception as e:
        return errorHandler('failed to upload Image. Error: '+str(e))

#get user
@app.route('/<user_type>/user', methods=['GET'])
@jwt_required()
def getUser(user_type):
    if user_type not in ['department','civilian']:
        return errorHandler('Invalid URL')

    token = request.headers['authorization']
    user_id = getUserFromHeader(token)

    query = f"SELECT email,name,added_by,phone_number,user_type,added_on FROM {'app_user' if user_type == 'civilian' else 'dep_app_user'} WHERE id_app_user = "+str(user_id)
    data = getServerData(query)

    dataJson = _dataframeToJson_(data)

    return responseWrapper(dataJson)

#get master data
@app.route('/master_data', methods=['GET'])
@jwt_required()
def getMasterData():
    mdata = masterData()
    return responseWrapper(mdata)

if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=8082)
    # app.run(debug=True, port='81', host ='0.0.0.0')
    app.run()