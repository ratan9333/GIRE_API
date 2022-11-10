from helpers.misc.connection import getServerData

def masterData():
    tables = ["m_designation","m_landuse_pattern","m_hotspot","m_junc_type","m_junc_formation","m_stretch_type","m_stretch_shape","no_of_lanes","m_nature_of_spot","m_landmark_type","m_vehicle_type","m_lighting_availability","m_switching_type","m_electrical_supply","m_spot_visibility","m_obstruction_for_driver","m_road_engineering_suggestions","m_is_accident_occured","m_defects","m_road_condition_solutions","m_user_violation_enforcement_solutions","m_road_user_violations","m_rash_drivers","m_rash_driving_enforcement_solutions"]
    masterData = {}
    for table in tables:
        query = f"SELECT {table}_id,{table}_value FROM {table} ORDER BY {table}_id ASC;"
        data = getServerData(query)
        masterData[table] = list(data[table+'_value'])
    return masterData