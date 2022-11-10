import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendOtp(otp,receiver_address):
    mail_content = "One Time Password to change your password is "+str(otp)
    #The mail addresses and password
    sender_address = 'support@akara.co.in'
    sender_pass = 'Supp3101@akaragg'
    # receiver_address = email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'CoERS - Forget Password - OTP'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()