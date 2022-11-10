from helpers.misc.connection import getServerData
from helpers.misc.helpers import responseWrapper


def getSurveyCounts():
    q1 = "SELECT COUNT(*) as count FROM dep_app_user" 
    q1_data = getServerData(q1)

    q2 = """
    SELECT  DISTINCT(feedback_type),COUNT(feedback_type) AS count FROM s_feedback 
    INNER JOIN s_general on s_feedback.s_general_id = s_general.s_general_id
    GROUP BY feedback_type
    """ 
    q2_data = getServerData(q2)

    q3 = "SELECT COUNT(*) as count FROM f_survey_general_details" 
    q3_data = getServerData(q3)

    data = {}
    data['department_user_count'] = int(q1_data['count'][0])
    data['appreciation_feedback_count'] = int(list(q2_data[q2_data['feedback_type'] == 2]['count'])[0])
    data['complaint_feedback_count'] = int(list(q2_data[q2_data['feedback_type'] == 1]['count'])[0])
    data['field_survey_count'] = int(q3_data['count'][0])

    return responseWrapper(data)