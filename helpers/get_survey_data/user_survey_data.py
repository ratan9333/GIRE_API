from helpers.misc.connection import getServerData
import pandas as pd

def user_survey_data(user_id,user_type):
    print('user_id: ',user_id)
    if user_type == 'civilian':
        s_table_name = 's_general'
        f_table_name = 's_feedback'
    else:
        s_table_name = 's_general'
        f_table_name = 's_feedback'
        
    query = f"""
        SELECT * FROM
        (SELECT s_feedback_id,comment,m_feedback_id,added_on AS taken_on,s_general_id,m_feedback_other FROM {f_table_name} 
        WHERE s_general_id IN (SELECT s_general_id FROM {s_table_name} WHERE added_by = {user_id})) t1
        INNER JOIN
        (SELECT s_general_id,
        CASE
            WHEN feedback_type = 2 THEN 'Appreciation'
            ELSE 'Complaint'
        END AS feedback_type
        FROM {s_table_name} WHERE added_by = {user_id}) t2
        ON t1.s_general_id = t2.s_general_id
        INNER JOIN
        (SELECT m_bad_road_type_list_value AS type,m_bad_road_type_list_id FROM m_bad_road_type_list) t3
        ON t1.m_feedback_id = t3.m_bad_road_type_list_id
        INNER JOIN
        (SELECT m_good_road_type_list_value AS good_type,m_good_road_type_list_id FROM m_good_road_type_list) t4
        ON t1.m_feedback_id = t4.m_good_road_type_list_id
        ORDER BY taken_on DESC
    """
    data = getServerData(query)
    if len(data) == 0:
        return pd.DataFrame()
    for i in range(len(data)):
        if data['feedback_type'][i] == 'Appreciation':
            good_value = data['good_type'][i]
            print(good_value)
            data.at[i,'type'] = good_value

    data = data[['s_feedback_id','type','comment','taken_on','feedback_type','m_feedback_other']]
    return data