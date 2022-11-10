import datetime
from flask import Flask, request,jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from psycopg2 import Date
from helpers.get_survey_data.get_all_survey_data import getAllSurveyData
from helpers.get_survey_data.get_f_survey_data import get_feedback_data
from helpers.get_survey_data.get_one_survey_data import *
from helpers.get_survey_data.user_survey_data import user_survey_data
from helpers.images.send_images import getImages
from helpers.map_data import  map_data
# from helpers.images.send_images import get_response_image
from helpers.misc.helpers import *
from helpers.misc.connection import *
from helpers.misc.decodeToken import getUserFromHeader
from helpers.misc.helpers import _dataframeToJson_
from helpers.master_data.master_data import masterData
from helpers.otp.generate_otp import changePassword, generateOtp
from helpers.signup.social_user import socialUser
from helpers.survey_counts import getSurveyCounts
from helpers.upload_data.upload_data import sqlUpload
from helpers.login.user_login import *
from helpers.signup.create_user import *
from datetime import date, timedelta
from waitress import serve
import os

from helpers.upload_data.upload_survey import uploadSurveyData

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = '123456'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1440)
jwt = JWTManager(app)

@app.route('/<user_type>/login', methods=['POST'])
def login(user_type):
    if user_type not in ['department', 'civilian']:
        return errorHandler('Invalid URL')
    try:
        bodyData = request.get_json()
        if bodyData == None:
            return errorHandler('Missing Required Params')
    except:
        return errorHandler('Missing Data')
    return userLogin(bodyData, user_type)


@jwt_required
@app.route('/department/users', methods=['GET'])
def getAllUsers():
    try:
        query = 'SELECT id_app_user, added_on, name, email, phone_number,m_designation_id,m_department_id,m_user_type_id FROM  dep_app_user WHERE is_deleted = 0'
        data = getServerData(query)
        print('called')

        return responseWrapper(_dataframeToJson_(data))
    except Exception as e:
        return errorHandler(str(e))

@jwt_required
@app.route('/department/users/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    try:
        query = f"UPDATE app_user SET is_deleted = 1 WHERE id_app_user = {user_id}"
        connection = engine.connect()
        connection.execute(query)
        connection.close()
        return responseWrapper({})
    except Exception as e:
        return errorHandler(str(e))


@app.route('/<user_type>/signup', methods=['POST'])
def User(user_type):
    if user_type not in ['department', 'civilian', 'social']:
        return errorHandler('Invalid URL')
    if request.method == 'POST':
        bodyData = request.get_json()
        if user_type in ['department', 'civilian']:
            return createUser(bodyData, user_type)
        else:
            return socialUser(bodyData)

# upload data


@app.route('/<user_type>/<data_type>', methods=['POST'])
@jwt_required()
def uploadData(user_type, data_type):
    if user_type not in ['department', 'civilian']:
        return errorHandler('Invalid URL')

    bodyData = request.get_json()
    user_id = getUserFromHeader(request.headers['authorization'])

    if data_type == 'feedback':
        data = sqlUpload(bodyData, user_id, user_type)
        return responseWrapper(data)
    if data_type == 'field_survey':
        if user_type not in ['department']:
            return errorHandler('Invalid URL')
        return uploadSurveyData(bodyData, user_id, user_type)

# upload documents


@app.route('/<user_type>/upload_documents', methods=['POST'])
@jwt_required()
def uploadDocuments(user_type):
    if user_type not in ['department', 'civilian']:
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

        return {"msg": "document uploaded successfully"}
    except Exception as e:
        return errorHandler('failed to upload document. Error: '+str(e))

# upload Pictures


@app.route('/<user_type>/upload_image', methods=['POST'])
@jwt_required()
def uploadPictures(user_type):
    if user_type not in ['department', 'civilian']:
        return errorHandler('Invalid URL')
    print('aa')

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
        print(document_folders)
        if file_name in document_folders:
            return errorHandler("Image Name already exists")
            # os.mkdir(doc_path+'/'+str(user_id))

        file.save(doc_path+'/'+file_name)

        return {"msg": "Image uploaded successfully"}
    except Exception as e:
        return errorHandler('failed to upload Image. Error: '+str(e))

# get user


@app.route('/<user_type>/user', methods=['GET'])
@jwt_required()
def getUser(user_type):
    if user_type not in ['department', 'civilian']:
        return errorHandler('Invalid URL')

    token = request.headers['authorization']
    user_id = getUserFromHeader(token)

    query = f"SELECT email,name,added_by,phone_number,user_type,added_on FROM {'app_user' if user_type == 'civilian' else 'app_user'} WHERE id_app_user = "+str(
        user_id)
    data = getServerData(query)

    dataJson = _dataframeToJson_(data)

    return responseWrapper(dataJson)

# get master data


@app.route('/master_data', methods=['GET'])
def getMasterData():
    mdata = masterData()
    return responseWrapper(mdata)

# send survey data


@jwt_required()
@app.route('/survey_data', methods=['POST'])
def getSurveyData():
    from_date, to_date = request.args.get(
        'from_date'), request.args.get('to_date')

    return getAllSurveyData(from_date, to_date)

# send user survey data


@app.route('/<user_type>/user_feedback', methods=['GET'])
def user_feedback_data(user_type):
    if user_type not in ['department', 'civilian']:
        return errorHandler('Invalid URL')

    token = request.headers['authorization']
    user_id = getUserFromHeader(token)

    data = _dataframeToJson_(user_survey_data(user_id, user_type))
    return responseWrapper(data)


# send survey data
@app.route('/appreciation_feedback_data', methods=['GET'])
def appreciation_feedback_data():
    return get_feedback_data(2, None, None, None)


@app.route('/complaint_feedback_data', methods=['GET'])
def complaint_feedback_data():
    return get_feedback_data(1, None, None, None)

@app.route('/feedback_data', methods=['POST'])
def feedback_data():
    bodyData = request.get_json()
    from_date = bodyData.get('from_date')
    to_date = bodyData.get('to_date')
    feedback_type = bodyData.get('feedback_type')
    user_id = bodyData.get('user_id')
    from_date = datetime.datetime.now() - datetime.timedelta(days=3*365).strftime(
        '%Y-%m-%d') if from_date is None else from_date
    to_date = date.today().strftime('%Y-%m-%d') if to_date is None else to_date

    query = f"""
        SELECT  m_feedback_id, s_feedback_id, s_feedback.added_on, m_feedback_other, feedback_type, name as added_by, `comment` FROM s_feedback 
        INNER JOIN s_general on s_feedback.s_general_id = s_general.s_general_id
        INNER JOIN app_user ON s_feedback.added_by = app_user.id_app_user
        WHERE s_feedback.added_on BETWEEN '{from_date}' AND '{to_date}'
        {f"AND added_by = {user_id}" if user_id != None else ""} 
        {f"AND feedback_type = {feedback_type}" if feedback_type != None else ""} 
        ORDER BY s_feedback.added_on DESC
    """

    data = getServerData(query)
    dataJson = _dataframeToJson_(data)
    return responseWrapper(dataJson)


@app.route('/web/feedback_data', methods=['POST'])
def appreciation_feedback_dat():
    bodyData = request.get_json()

    from_date = bodyData.get('from_date')
    to_date = bodyData.get('to_date')
    feedback_type = bodyData.get('feedback_type')
    user_id = bodyData.get('user_id')

    return get_feedback_data(feedback_type=feedback_type, user_id=user_id, from_date=from_date, to_date=to_date)


@app.route('/get_otp', methods=['GET'])
def get_otp():
    bodyData = request.get_json()

    email = bodyData['email']
    password = bodyData['password']

    return generateOtp(email,password)

@app.route('/change_password', methods=['GET'])
def change_password():
    bodyData = request.get_json()

    email = bodyData['email']
    otp = bodyData['otp']
    new_pass = bodyData['password']

    return changePassword(email,otp,new_pass)

@app.route('/feedback_images/<s_feedback_id>',methods=['GET'])
def get_images(s_feedback_id):
    data = getImages(s_feedback_id)
    return responseWrapper(data)

@app.route('/map_data',methods=['POST'])
def get_map_data():
    bodyData = request.get_json()

    if "from_date" in bodyData:
        from_date = bodyData['from_date']
    else:
        from_date = '2022-01-01'

    if "to_date" in bodyData:
        to_date = bodyData['to_date']
    else:
        to_date = '2030-01-01'

    if "complaint_types" in bodyData:
        complaint_types = bodyData['complaint_types']
    else:
        complaint_types = None

    if "appreciation_types" in bodyData:
        appreciation_types = bodyData['appreciation_types']
    else:
        appreciation_types = None

    if "field_survey" in bodyData:
        field_survey = bodyData['field_survey']
    else:
        field_survey = False
        
    data = map_data(from_date,to_date,complaint_types,appreciation_types,field_survey)

    return responseWrapper(data)

@app.route('/feedback/<feedback_id>',methods=['GET'])
def one_feedback_data(feedback_id):
    return getOneFeedbackData(feedback_id)

@app.route('/survey/<survey_id>',methods=['GET'])
def one_survey_data(survey_id):
    return getOneSurveyData(survey_id)

@app.route('/dashboard_data',methods=['GET'])
def survey_count():
    return getSurveyCounts()

if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=8082)
    app.run(debug=True, port='8082', host='0.0.0.0')
    # app.run()
