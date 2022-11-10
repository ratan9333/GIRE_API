import queue
from helpers.master_data.master_data import masterData

from helpers.misc.connection import getServerData
from helpers.misc.helpers import _dataframeToJson_, responseWrapper


def getAllSurveyData(from_date, to_date):

    date_filter = f"AND added_on BETWEEN '{from_date}' AND '{to_date}'" if from_date != None else ''

    # master_data = masterData()
    survey_tables = ["f_survey_general_details", "f_survey_road_details", "f_survey_traffic_conditions", "f_survey_traffic_signal_status",
                     "f_survey_lighting_condition", "f_survey_visibility", "f_survey_road_condition", "f_survey_rash_driving_pattern", "f_survey_road_user_violation"]
    drop_columns = ['is_deleted', 'updated_by', 'updated_on', 'nano_id', 'photos', 'visibility_photos',
                    'road_marking_photos', 'lighting_photos', 'road_condition_photos', "signal_photos", "signboard_photos"]
    all_survey_ids = []
    final_survey_data = {}
    for eachSurveyTable in survey_tables:
        query = f"SELECT * FROM {eachSurveyTable} {date_filter} ORDER BY added_on DESC"
        data = getServerData(query)
        for eachDropColumn in drop_columns:
            try:
                for eachColumn in list(data.columns):
                    if eachColumn in drop_columns:
                        data = data.drop(columns=[eachDropColumn])
                    elif 'photos' in eachColumn:
                        print(eachColumn)
                        data = data.drop(columns=[eachDropColumn])
            except:
                pass

        if eachSurveyTable == "f_survey_general_details":
            for i in range(len(data)):
                final_data = {}
                survey_id = int(data['f_survey_general_details_id'][i])
                final_survey_data[survey_id] = {}
                final_survey_data[survey_id][eachSurveyTable] = _dataframeToJson_(data.loc[[i]])[
                    0]
                all_survey_ids.append(survey_id)

        else:
            for eachSurvey_id in all_survey_ids:
                survey_data = data[data['f_survey_general_details_id']
                                   == eachSurvey_id]
                if len(survey_data) == 0:
                    final_survey_data[eachSurvey_id][eachSurveyTable] = {}
                else:
                    survey_data.reset_index(inplace=True, drop=True)

                    final_survey_data[eachSurvey_id][eachSurveyTable] = _dataframeToJson_(survey_data)[
                        0]

                # final_survey_data.append(final_data)

    return responseWrapper(list(final_survey_data.values()))
