import json
import sys
import subprocess
import os
import random
import time
import commands
import string

from db_connection import get_all_requests_from_db
from db_connection import change_status_in_db


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def write_log(data):
    base_dir = os.path.dirname(CURRENT_DIR)
    with open(os.path.join(base_dir,'logs', 'log.txt'), 'a') as txt_file:
        txt_file.write(str(data) + 'n')


def set_current_count(count):
    try:
        STATUS_FILE = os.path.join(CURRENT_DIR, 'scan_status.json')
        json_file = open(STATUS_FILE, 'wb')
        status = {'current_count':str(count)}
        json.dump(status, json_file)
        json_file.close()
    except Exception, e:
        print str(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))


def get_current_count():
    try:
        STATUS_FILE = os.path.join(CURRENT_DIR, 'scan_status.json')
        json_file = open(STATUS_FILE, 'rb')
        status = json.load(json_file)
        json_file.close()
        return int(status['current_count'])
    except Exception, e:
        print str(e)
        change_status_in_db('NOT STARTED', request['location'])
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))

def increase_current_count_by_one():
    current_count = get_current_count()
    set_current_count(current_count + 1)


def decrease_current_count_by_one():
    current_count = get_current_count()
    set_current_count(current_count - 1)


def shallow_extract_and_delete(input_zip):
    try:
        if input_zip.endswith('.zip') and os.path.exists(input_zip):
            commands.getstatusoutput('unzip ' + input_zip + ' -d' + os.path.dirname(input_zip))
            os.remove(input_zip)
    except Exception, e:
        print str(e)
        change_status_in_db('NOT STARTED')
        decrease_current_count_by_one()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))


def get_random_chars(length=5):
    chars = []
    for i in range(length):
        chars.append(random.choice(string.ascii_letters))
    return ''.join(chars)


def create_temp_directory(dirname):
    try:
        location = os.path.join('/tmp/', dirname)
        if not os.path.exists(location):
            os.mkdir(location)
        return location
    except Exception, e:
        print str(e)
        decrease_current_count_by_one()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))

def run_scan_app(infos):
    try:
        if infos:
            dir_name = get_random_chars()
            temp_dir = create_temp_directory(dir_name)
            request_file = os.path.join(temp_dir, dir_name+'.json')
            infos['working_dir'] = temp_dir
            with open(request_file, 'wb') as json_file:
                json.dump(infos, json_file)
            subprocess.Popen('python ' + os.path.join(CURRENT_DIR, 'scanner.py') +' ' + request_file, stdout=subprocess.PIPE, shell=True)
    except Exception, e:
        print str(e)
        decrease_current_count_by_one()
        change_status_in_db('NOT STARTED', infos['location'])
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))


while True:
    infos = get_all_requests_from_db()
    current_count = get_current_count()
    if not infos:
        break
    elif current_count < 5 and len(infos)>0:
        request = infos[0]
        change_status_in_db('STARTED', request['location'])
        increase_current_count_by_one()
        run_scan_app(request)
        time.sleep(10)
