import json
from helpers.misc.connection import executeQuery, getServerData

def sqlUploadDataQuery(table_name,data):

    for eachKey in data.keys():
        value = data[eachKey]
        if isinstance(value,dict):
            value = json.dumps(value)
            data[eachKey] = value

        elif isinstance(value,list):
            newList = []
            for eachValue in value:
                if isinstance(eachValue,dict):
                    changedValue = json.dumps(eachValue)
                    newList.append(changedValue)
                else:
                    newList.append(eachValue)
            print('new list: ',newList)
            data[eachKey] = str(newList).replace("'",'')
        elif isinstance(value,int):
            data[eachKey] = value
        elif value in [True,False]:
            value = 'Y' if value == True else 'N'
            data[eachKey] = value


    query = 'INSERT INTO '+table_name+' (`'
    query += '`,`'.join(list(data.keys()))
    query += '`) VALUES('+"'"
    query += "','".join([str(x) for x in list(data.values())])
    query += "');"
    print(query)
    return query

def sqlUpload(data,user_id,user_type):

    if user_type == 'civilian':
        sgeneral_tname = 's_general'
        sfeedback_tname = 's_feedback'
        sdocuments_tname = 's_documents'
    else:
        sgeneral_tname = 's_general'
        sfeedback_tname = 's_feedback'
        sdocuments_tname = 's_documents'


    # Upload S general
    s_general_data = data['s_general']
    s_general_data['added_by'] = user_id
    s_general_query = sqlUploadDataQuery(sgeneral_tname,s_general_data)
    executeQuery(s_general_query)

    #fetch the last s_general_id
    s_general_id_query = f"SELECT max(s_general_id) as new_key FROM `{sgeneral_tname}`;" 
    s_general_id = getServerData(s_general_id_query)['new_key'][0]
    
    #Upload Feedback and Documents Data
    s_feedback_data = data['s_feedback']
    feedbacks = []
    for eachFeedback in s_feedback_data:
        s_documents_data = eachFeedback['documents']

        each_s_feedback_data = eachFeedback
        del each_s_feedback_data['documents']

        each_s_feedback_data['s_general_id'] = s_general_id
        each_s_feedback_data['added_by'] = user_id
        feedback_query = sqlUploadDataQuery(sfeedback_tname,each_s_feedback_data)
        executeQuery(feedback_query)

        # get s_feedback_id
        s_feedback_id_query = f"SELECT nano_id,s_feedback_id FROM {sfeedback_tname} WHERE s_feedback_id = (SELECT MAX(s_feedback_id) FROM {sfeedback_tname})" 
        s_feedback_id = getServerData(s_feedback_id_query)
        temp_s_feedback_id = int(s_feedback_id['s_feedback_id'][0])
        temp_s_nano_id = (s_feedback_id['nano_id'][0])

        # upload documents data
        feedback_vs_docids = {}
        no_of_docs = len(list(s_documents_data))
        for eachDocument in s_documents_data:
            doc_data = eachDocument
            doc_data['added_by'] = user_id
            doc_data['s_feedback_id'] = temp_s_feedback_id

            doc_query = sqlUploadDataQuery(sdocuments_tname,doc_data)
            executeQuery(doc_query)

            document_ids_query = f"SELECT nano_id,s_document_id FROM {sdocuments_tname} ORDER BY s_document_id DESC LIMIT "+str(no_of_docs)
            print(document_ids_query)
            document_ids = getServerData(document_ids_query)
            # document_ids_map = []
            document_ids_map = {}
            document_ids_map['id'] = temp_s_feedback_id
            document_ids_map['docs'] = {}
            for i in range(len(document_ids)):
                document_ids_map['docs'][document_ids['nano_id'][i]] = int(document_ids['s_document_id'][i])
            # document_ids_map.append(temp)
            # feedback_vs_docids[s_feedback_id] = document_ids
            feedback_vs_docids[temp_s_nano_id] = document_ids_map

        feedbacks.append({'s_general_id':int(s_general_id),'s_feedback_ids':feedback_vs_docids})
    return feedbacks
