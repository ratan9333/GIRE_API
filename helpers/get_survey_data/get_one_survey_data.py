from helpers.misc.connection import getServerData
from helpers.misc.helpers import responseWrapper

def getOneFeedbackData(feedback_id):
    query = f"""
    SELECT m_feedback_id,m_feedback_other,comment,added_on,name,feedback_type,latitude,longitude
    FROM s_feedback
    LEFT JOIN 
    (SELECT app_user.id_app_user,app_user.name FROM app_user) app_user 
    ON s_feedback.added_by = app_user.id_app_user
    LEFT JOIN 
    (SELECT s_general.feedback_type,s_general.s_general_id,latitude,longitude FROM s_general) s_general
    ON s_general.s_general_id = s_feedback.s_general_id
    WHERE s_feedback.s_feedback_id = {feedback_id}
    """
    data = getServerData(query)

    if len(data) == 0:
        return responseWrapper({})
    else:
        response = {}
        for i in list(data.columns):
            try:
                response[i] = float(data[i][0])
            except:
                response[i] = str(data[i][0])

        return responseWrapper(response)

def getOneSurveyData(survey_id):
    query = f"""
    SELECT f_survey_general_details.f_survey_general_details_id,repr_name,m_designation_value,phone_number,added_on,peak_hours,department,
    is_signal_available,is_signal_visible,is_signal_working,NAME
    FROM f_survey_general_details
    LEFT JOIN (SELECT f_survey_general_details_id,peak_hours FROM f_survey_traffic_conditions)f_survey_traffic_conditions 
    ON f_survey_general_details.f_survey_general_details_id = f_survey_traffic_conditions.f_survey_general_details_id
    LEFT JOIN
    (SELECT f_survey_general_details_id,is_signal_available,is_signal_visible,is_signal_working 
    FROM f_survey_traffic_signal_status) f_survey_traffic_signal_status
    ON f_survey_traffic_signal_status.f_survey_general_details_id = f_survey_general_details.f_survey_general_details_id
    LEFT JOIN (SELECT id_app_user,NAME FROM app_user) app_user
    ON app_user.id_app_user = f_survey_general_details.added_by
    LEFT JOIN 
    (SELECT m_designation_value,m_designation_id FROM m_designation) m_designation
    ON m_designation.m_designation_id = f_survey_general_details.designation_id
    WHERE f_survey_general_details.f_survey_general_details_id = {survey_id}
    """
    data = getServerData(query)

    print(query)

    if len(data) == 0:
        return responseWrapper({})
    else:
        response = {}
        for i in list(data.columns):
            try:
                response[i] = float(data[i][0])
            except:
                if i != 'peak_hours':
                    response[i] = str(data[i][0])
                else:
                    response[i] = (data[i][0])

        return responseWrapper(response)