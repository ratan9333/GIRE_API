from helpers.misc.connection import getServerData
from helpers.misc.helpers import _dataframeToJson_, errorHandler, responseWrapper
from datetime import datetime


def get_feedback_data(feedback_type, user_id, from_date, to_date):
    from_date = datetime.today().strftime(
        '%Y-%m-%d') if from_date is None else from_date
    to_date = datetime.today().strftime('%Y-%m-%d') if to_date is None else to_date

    print(from_date, to_date)

    s_general_query = f"""
    SELECT added_by,added_on,altitude,feedback_type,latitude,longitude,s_general_id FROM s_general 
    WHERE added_on BETWEEN '{from_date}' AND '{to_date}'
    {f"AND added_by = {user_id}" if user_id != None else ""} 
    {f"AND feedback_type = {feedback_type}" if feedback_type != None else ""} 
    """

    print(s_general_query)

    s_general_data = getServerData(s_general_query)

    if s_general_data.empty:
        return responseWrapper([])

    survey_ids = list(s_general_data['s_general_id'].unique())
    if len(survey_ids) == 0:
        survey_ids_for_query = ''
    else:
        survey_ids_for_query = ','.join([str(x) for x in survey_ids])

    s_feedback_query = f"SELECT added_by,added_on,comment,m_feedback_id,m_feedback_other,s_feedback_id,s_general_id FROM s_feedback WHERE s_general_id in ({survey_ids_for_query})"
    s_feedback_data = getServerData(s_feedback_query)

    s_feedback_ids = list(s_feedback_data['s_feedback_id'].unique())
    if len(s_feedback_ids) == 0:
        s_feedback_ids_for_query = ''
    else:
        s_feedback_ids_for_query = ','.join([str(x) for x in s_feedback_ids])

    s_documents_query = f"SELECT added_by,added_on,altitude,f_survey_general_details_id,file_name,file_path,latitude,longitude,photo_taken_at,s_document_id,s_feedback_id FROM s_documents WHERE s_feedback_id in ({s_feedback_ids_for_query})"
    s_documents_data = getServerData(s_documents_query)

    survey_data = {}

    # add sgeneral data
    for eachSurvey in survey_ids:
        survey_data[int(eachSurvey)] = {}
        eachSurveyData = s_general_data[s_general_data['s_general_id'] == eachSurvey]
        eachSurveyData.reset_index(inplace=True, drop=True)
        survey_data[eachSurvey]['s_general'] = _dataframeToJson_(eachSurveyData)[
            0]

    # add feedback
    for eachSurvey in survey_ids:
        # survey_data[int(eachSurvey)]['s_feedback'] = []
        eachSurveyFeedback = s_feedback_data[s_feedback_data['s_general_id'] == eachSurvey]
        eachSurveyFeedback.reset_index(inplace=True, drop=True)
        survey_data[int(eachSurvey)]['s_feedback'] = _dataframeToJson_(
            eachSurveyFeedback)

    # add s_documents
    for eachSurvey in survey_ids:
        s_feeback_documents_added_data = []
        for eachFeedback in survey_data[int(eachSurvey)]['s_feedback']:
            eachFeedbackId = eachFeedback['s_feedback_id']
            eachFeedback_documents = s_documents_data[s_documents_data['s_feedback_id'] == int(
                eachFeedbackId)]
            eachFeedback_documents.reset_index(inplace=True, drop=True)

            eachFeedback['s_documents'] = _dataframeToJson_(
                eachFeedback_documents)

            s_feeback_documents_added_data.append(eachFeedback)
        survey_data[int(eachSurvey)
                    ]['s_feedback'] = s_feeback_documents_added_data

    return responseWrapper(list(survey_data.values()))



def get_one_feedback_data(s_general_id):

    s_general_query = f"""
    SELECT added_by,added_on,altitude,feedback_type,latitude,longitude,s_general_id FROM s_general 
    WHERE s_general_id = {s_general_id}
    """

    print(s_general_query)

    s_general_data = getServerData(s_general_query)

    if s_general_data.empty:
        return responseWrapper([])

    survey_ids = list(s_general_data['s_general_id'].unique())
    if len(survey_ids) == 0:
        survey_ids_for_query = ''
    else:
        survey_ids_for_query = ','.join([str(x) for x in survey_ids])

    s_feedback_query = f"SELECT added_by,added_on,comment,m_feedback_id,m_feedback_other,s_feedback_id,s_general_id FROM s_feedback WHERE s_general_id in ({survey_ids_for_query})"
    s_feedback_data = getServerData(s_feedback_query)

    s_feedback_ids = list(s_feedback_data['s_feedback_id'].unique())
    if len(s_feedback_ids) == 0:
        s_feedback_ids_for_query = ''
    else:
        s_feedback_ids_for_query = ','.join([str(x) for x in s_feedback_ids])

    s_documents_query = f"SELECT added_by,added_on,altitude,f_survey_general_details_id,file_name,file_path,latitude,longitude,photo_taken_at,s_document_id,s_feedback_id FROM s_documents WHERE s_feedback_id in ({s_feedback_ids_for_query})"
    s_documents_data = getServerData(s_documents_query)

    survey_data = {}

    # add sgeneral data
    for eachSurvey in survey_ids:
        survey_data[int(eachSurvey)] = {}
        eachSurveyData = s_general_data[s_general_data['s_general_id'] == eachSurvey]
        eachSurveyData.reset_index(inplace=True, drop=True)
        survey_data[eachSurvey]['s_general'] = _dataframeToJson_(eachSurveyData)[
            0]

    # add feedback
    for eachSurvey in survey_ids:
        # survey_data[int(eachSurvey)]['s_feedback'] = []
        eachSurveyFeedback = s_feedback_data[s_feedback_data['s_general_id'] == eachSurvey]
        eachSurveyFeedback.reset_index(inplace=True, drop=True)
        survey_data[int(eachSurvey)]['s_feedback'] = _dataframeToJson_(
            eachSurveyFeedback)

    # add s_documents
    for eachSurvey in survey_ids:
        s_feeback_documents_added_data = []
        for eachFeedback in survey_data[int(eachSurvey)]['s_feedback']:
            eachFeedbackId = eachFeedback['s_feedback_id']
            eachFeedback_documents = s_documents_data[s_documents_data['s_feedback_id'] == int(
                eachFeedbackId)]
            eachFeedback_documents.reset_index(inplace=True, drop=True)

            eachFeedback['s_documents'] = _dataframeToJson_(
                eachFeedback_documents)

            s_feeback_documents_added_data.append(eachFeedback)
        survey_data[int(eachSurvey)
                    ]['s_feedback'] = s_feeback_documents_added_data

    return responseWrapper(list(survey_data.values()))
