import io
from base64 import encodebytes
import os
from PIL import Image
from flask import jsonify
from helpers.misc.connection import getServerData

def get_response_image(image_path):
    # try:
    import base64

    with open('images/civilian/'+image_path,"rb") as image_file:
        contents = image_file.read()
        encoded_string = base64.b64encode(contents)

        return str(encoded_string)[2:-1]

    # pil_img = Image.open('images/civilian/'+image_path, mode='r') # reads the PIL image
    # byte_arr = io.BytesIO()
    # if 'png' in image_path:
    #     img_ext = 'PNG'
    # elif 'jpg' in image_path:
    #     img_ext = 'JPG'
    # elif 'jpeg' in image_path:
    #     img_ext = 'JPEG'
    
    # pil_img.save(byte_arr, format='JPG') # convert the PIL image to byte array
    # encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    # return encoded_img
    # except:
    #     return ''

def getImages(s_feedback_id):
    query = f"SELECT file_name,latitude,longitude,photo_taken_at,altitude,s_document_id FROM s_documents WHERE s_feedback_id = {s_feedback_id}"
    data = getServerData(query)

    result = list(data['file_name'])

    print(os.listdir('images/civilian'))

    if len(result) == 0:
        return []
    else:

        encoded_imges = []
        for i in range(len(data)):
                # try:
                temp = {}   
                img_name = str(data['s_document_id'][i])+"_"+str(data['file_name'][i])
                print("img_name",img_name)
                temp['img'] = get_response_image(img_name)
                temp['file_name'] = data['file_name'][i]
                temp['latitude'] = data['latitude'][i]
                temp['longitude'] = data['longitude'][i]
                temp['photo_taken_at'] = data['photo_taken_at'][i]
                temp['altitude'] = data['altitude'][i]

                encoded_imges.append(temp)
                # except:
                #     pass

        return encoded_imges
        