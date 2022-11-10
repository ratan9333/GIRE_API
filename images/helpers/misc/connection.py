import pandas as pd
from urllib.parse import quote  

def serverConnection():
    import helpers.misc.server_credentials as sc
    from sqlalchemy import create_engine
    engine = create_engine('mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{db}'
                           .format(
                               user=sc.user,
                               passwd=sc.passwd,
                               host=sc.host,
                               port=sc.port,
                               db=sc.db_name
                           ))

    return engine


engine = serverConnection()

def getServerData(query):
    connection = engine.connect()
    tmp = connection.execute(query)
    data = pd.DataFrame()
    while True:
        partial_results = tmp.fetchmany(10000)
        if (len(partial_results) == 0):
            break
        res = pd.DataFrame(partial_results)
        res.columns = partial_results[0].keys()
        data = data.append(res)
    connection.close()
    return data

def executeQuery(query):
    connection = engine.connect()
    connection.execute(query)
    connection.close()