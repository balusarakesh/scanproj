import MySQLdb
import os
from boto.s3.key import Key
import sys
import boto
#FIXME
# from scanproj.scanproj import external_db



def get_connector(user=NAME,passwd=PASSWORD,host=HOST,db=NAME):
    """
    Returns a connector for a given database by using the parameters 'user', 'passwd', 'host' and 'db',
    """
    try:
        conn = MySQLdb.connect(user=user,passwd=passwd,host=host,db=db)
        return conn
    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        print error_msg
        print str(e)

def get_all_requests_from_db(query='Select * from scanapp_scanmodel where status="NOT STARTED"'):
    try:
        connector = get_connector()
        mycursor = connector.cursor()
        mycursor.execute(query)
        requests = mycursor.fetchall()
        infos = []
        if requests:
            for i in range(len(requests)):
                tmp = {}
                tmp['pk'] = requests[i][0]
                tmp['email'] = requests[i][1]
                tmp['resultsurl'] = requests[i][2]
                tmp['status'] = requests[i][3]
                tmp['location'] = requests[i][4]
                infos.append(tmp)
        connector.close()
        return infos
    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        print error_msg
        print str(e)


def change_status_in_db(status, location):
    try:
        connector = get_connector()
        mycursor = connector.cursor()
        mycursor.execute("update scanapp_scanmodel set status='%s' where location='%s'" %(status, location))
        connector.commit()
        mycursor.close()
        connector.close()
        
    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        print error_msg


def get_infos_from_db(location):
    try:
        connector = get_connector()
        mycursor = connector.cursor()
        if location:
            mycursor.execute('Select * from scanapp_scanmodel where location = "' + location + '"' )
        else:
            return
        request = mycursor.fetchall()[0]
        tmp = {}
        if request:
            tmp['pk'] = request[0]
            tmp['email'] = request[1]
            tmp['resultsurl'] = request[2]
            tmp['status'] = request[3]
            tmp['location'] = request[4]
        connector.close()
        return tmp
    except Exception, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        print error_msg


def upload_to_s3(location):
    conn = boto.connect_s3()
    if os.path.exists(location):
        bucket = conn.get_bucket(BUCKET_NAME)
        key = Key(bucket)
        key.key = os.path.basename(location)
        key.set_contents_from_file(open(location, 'rb'))
        key.set_acl('public-read')

