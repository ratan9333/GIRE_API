from helpers.misc.connection import executeQuery, getServerData
from helpers.misc.helpers import responseWrapper
from helpers.upload_data.upload_data import sqlUploadDataQuery

def getUploadId(tname):
    query = f"SELECT MAX({tname}_id) as id FROM {tname};"
    id = getServerData(query)['id'][0]
    return int(id)

def uploadSurveyData(bodyData,user_id,user_type):
    if user_type == 'department':
        general_tname = 'f_survey_general_details'
        spot_details_tname = 'f_survey_spot_details'
        traffic_conditions_tname = 'f_survey_traffic_conditions'
        traffic_signal_tname = 'f_survey_traffic_signal_status'
        lighting_condition_tname = 'f_survey_lighting_condition'
        visibility_tname = 'f_survey_visibility'
        road_condition_tname = 'f_survey_road_condition'
        rash_driving_pattern_tname = 'f_survey_rash_driving_pattern'
        road_user_violation_tname = 'f_survey_road_user_violation'

    # Upload s general data and get s general id
    general_data = bodyData['f_survey_general_details']
    general_data['added_by'] = user_id
    query = sqlUploadDataQuery(general_tname,general_data)
    print(query)
    executeQuery(query)

    f_survey_general_details_id = getUploadId(general_tname)

    # Upload f_survey_spot_details
    f_survey_spot_details_id = uploadTableData(spot_details_tname,bodyData,user_id,f_survey_general_details_id)

    # Upload f_survey_traffic_conditions
    f_survey_traffic_conditions_id = uploadTableData(traffic_conditions_tname,bodyData,user_id,f_survey_general_details_id)

    # Upload f_survey_traffic_signal_status
    f_survey_traffic_signal_status_id = uploadTableData(traffic_signal_tname,bodyData,user_id,f_survey_general_details_id)

    # Upload f_survey_lighting_condition
    f_survey_lighting_condition_id = uploadTableData(lighting_condition_tname,bodyData,user_id,f_survey_general_details_id)

    # Upload f_survey_visibility
    f_survey_visibility_id = uploadTableData(visibility_tname,bodyData,user_id,f_survey_general_details_id)

    # Upload f_survey_road_conidtion
    f_survey_road_condition_id = uploadTableData(road_condition_tname,bodyData,user_id,f_survey_general_details_id)

    # Upload f_survey_rash_driving_pattern
    f_survey_rash_driving_pattern_id = uploadTableData(rash_driving_pattern_tname,bodyData,user_id,f_survey_general_details_id)

    # Upload f_survey_road_user_violation
    f_survey_road_user_violation_id = uploadTableData(road_user_violation_tname,bodyData,user_id,f_survey_general_details_id)

    return responseWrapper({'f_survey_general_details_id':int(f_survey_general_details_id),
                                'f_survey_spot_details_id':int(f_survey_spot_details_id),
                                    'f_survey_traffic_conditions_id':int(f_survey_traffic_conditions_id),
                                        'f_survey_traffic_signal_status_id':int(f_survey_traffic_signal_status_id),
                                            'f_survey_lighting_condition_id':int(f_survey_lighting_condition_id),
                                                'f_survey_visibility_id':int(f_survey_visibility_id),
                                                    'f_survey_road_condition_id':int(f_survey_road_condition_id),
                                                        'f_survey_rash_driving_pattern_id':int(f_survey_rash_driving_pattern_id),
                                                            'f_survey_road_user_violation_id':int(f_survey_road_user_violation_id)})

def uploadTableData(tname,bodyData,user_id,f_survey_general_details_id):
    uploadData = bodyData[tname]
    uploadData['added_by'] = user_id
    uploadData['f_survey_general_details_id'] = f_survey_general_details_id
    query = sqlUploadDataQuery(tname,uploadData)
    executeQuery(query)

    id = getUploadId(tname)
    return id