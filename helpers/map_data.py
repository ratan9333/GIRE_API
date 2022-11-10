from helpers.misc.connection import getServerData
from helpers.misc.helpers import responseWrapper

def listToQuery(list):
    query = "("
    for x in list:
        query+=str(x)+','
    query = query[:-1]+')'
    return query


def map_data(from_date,to_date,complaint_types,appreciation_types,field_survey):

    if field_survey:
        date_filter_query = f"f_survey_general_details.added_on BETWEEN '{from_date}' AND '{to_date}'" if from_date != None else ''

    date_filter_query2 = f"s_general.added_on BETWEEN '{from_date}' AND '{to_date}'" if from_date != None else ''

    complaint_types_query = f" AND m_feedback_id IN {listToQuery(complaint_types)} " if len(complaint_types) > 0 else ''
    appreciation_types_query = f" AND m_feedback_id IN {listToQuery(appreciation_types)} " if len(appreciation_types) > 0 else ''

    if field_survey:
        query = f"SELECT f_survey_general_details_id,latitude,longitude,added_on FROM f_survey_general_details WHERE {date_filter_query}"
        d1 = getServerData(query)

    query2 = f"SELECT s_general.s_general_id,latitude,longitude,s_general.added_on,s_feedback_id,feedback_type,m_feedback_id FROM s_general INNER JOIN s_feedback ON s_general.s_general_id = s_feedback.s_general_id WHERE {date_filter_query2} {complaint_types_query} {appreciation_types_query}"
    print(query2)
    d2 = getServerData(query2)

    data = []

    if field_survey:
        for i in range(len(d1)):
            temp = {}
            temp['latitude'] = d1['latitude'][i]
            temp['longitude'] = d1['longitude'][i]
            temp['added_on'] = d1['added_on'][i]
            temp['type'] = 'survey'
            temp['id'] = str(d1['f_survey_general_details_id'][i])
            data.append(temp)

    for i in range(len(d2)):
        temp = {}
        temp['latitude'] = d2['latitude'][i]
        temp['longitude'] = d2['longitude'][i]
        temp['added_on'] = d2['added_on'][i]
        if str(d2['feedback_type'][i]) == '1':
            temp['type'] = 'complaint'
        elif str(d2['feedback_type'][i]) == '2':
            temp['type'] = 'appreciation'

        temp['id'] = int(d2['s_feedback_id'][i])
        data.append(temp)
    print('len: ',len(data))
    return data


def getOneSurveyData(id):

    query = f"SELECT * FROM f_survey_general_details WHERE f_survey_general_details_id = {id}"
    d1 = getServerData(query)
    print(d1)
    data = {}

    for i in list(d1.columns):
        try:
            data[i] = float(d1[i][0])
        except:
            data[i] = str(d1[i][0])

    print(data)
    return responseWrapper(data)