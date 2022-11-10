import random as r
from helpers.login.user_login import getUserPass

from helpers.misc.connection import executeQuery, getServerData
from helpers.misc.helpers import errorHandler, getSignedJwt, passwordHasher, responseWrapper
from flask_jwt_extended import create_access_token
import bcrypt
import datetime

from helpers.otp.otp import sendOtp

def otpgen():
    otp=""
    for i in range(6):
        otp+=str(r.randint(1,9))
    return str(otp)

def generateOtp(email,password):

    query = f"""SELECT email,password FROM app_user WHERE email = '{email}' """
    print(query)

    data = getServerData(query)

    if len(data) == 0:
        return errorHandler('Invalid Email')

    else:
        
        server_password,user_id,user_name,user_type,email,photo_url,phone_number = getUserPass(email,'civilian')

        if server_password != None:
            if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(server_password, 'utf-8')):
                otp = otpgen()
                query = f"""INSERT INTO otps (email,otp) VALUES ('{email}','{otp}') """

                executeQuery(query)

                sendOtp(otp,email)

                return responseWrapper("OTP Sent Successfully. Please Check your Email.")
                
            else:
                return errorHandler('Password Incorrect')
        else:
            return errorHandler("Email dosen't Exist")

def changePassword(email,otp,new_pass):

    query = f"""SELECT email,otp,added_on FROM otps WHERE email = '{email}' """
    print(query)

    data = getServerData(query)

    if len(data) == 0:
        return errorHandler('Invalid Email')
    else:
        now = datetime.datetime.now() - datetime.timedelta(hours=5,minutes=30)
        time_diff = now - data['added_on'][max(list(data.index))]

        if (time_diff.total_seconds() / 60) > 10:
            return errorHandler("OTP Exipred")
        else:
            if str(otp) == str(data['otp'][max(list(data.index))]):

                tempPass = passwordHasher(new_pass)
                tempPass = tempPass.decode('utf-8')
                
                query = f""" UPDATE app_user SET password = '{str(tempPass)}' WHERE email = '{email}' """
                print(query)
                executeQuery(query)

                return responseWrapper("Password Changed Successfully")

            else:
                return errorHandler("Incorrect OTP")