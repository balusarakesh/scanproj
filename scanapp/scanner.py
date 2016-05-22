import json
import url
from db_connection import get_infos_from_db
import commands
import os
import subprocess
import shutil
from db_connection import change_status_in_db
from scan_helper import get_current_count
from scan_helper import set_current_count
from scan_helper import get_random_chars
from scan_helper import write_log
from db_connection import upload_to_s3
from scan_helper import decrease_current_count_by_one


PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANCODE_LOC = os.path.join(PROJ_DIR, 'scancode-toolkit/')

def create_zip_file(dirname, zip_name):
    try:
        if dirname and zip_name:
            if '.zip' in zip_name:
                zip_name = zip_name.replace('.zip', '')
            shutil.make_archive(os.path.join('/tmp/', zip_name), 'zip', dirname)
    except Exception, e:
        decrease_current_count_by_one
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))

def delete_directory(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)


def get_filename_from_url(input_url):
    if url.parse(input_url).absolute():
        return input_url.split('/')[-1]


def return_results(infos, message, working_dir):
    try:
        if working_dir:
            zip_name = get_filename_from_url(infos['resultsurl'])
            try:
                create_zip_file(working_dir, zip_name)
                delete_directory(working_dir)
            except Exception, e:
                write_log(str(e))
            infos = get_infos_from_db(location=infos['location'])
            count = get_current_count()
            set_current_count(count-1)
            change_status_in_db('FINISHED', infos['location'])
            upload_to_s3(os.path.join('/tmp/', zip_name ))
        else:
            change_status_in_db('ERROR', infos['location'])
    except Exception, e:
        decrease_current_count_by_one()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))

def get_file_name(location):
    try:
        file_loc = os.path.dirname(location)
        name = location.replace(file_loc, '')
        return name
    except Exception, e:
        decrease_current_count_by_one()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))


def get_file_name_with_no_ext(name):
    try:
        no_ext = name.split('.')[-2]
        if no_ext.startswith('/'):
            no_ext = no_ext[1:]
        return no_ext
    except Exception, e:
        decrease_current_count_by_one()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))


def configure_scancode(scancode_loc):
    result = commands.getstatusoutput(scancode_loc + './scancode --help')
    try:
        if result:
            return True
    except Exception, e:
        decrease_current_count_by_one
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))


def scan_in_sub_process(json_file):
    try:
        infos = json.loads(open(json_file, 'rb').read())
        os.remove(json_file)
        location = infos['location']
        working_dir = infos['working_dir']
    
        html_loc = os.path.join(working_dir, get_random_chars(5) + '.html')
        if configure_scancode(SCANCODE_LOC):
            scan_command = 'scancode --format=html-app --license --copyright '+location + ' ' + html_loc
            process = subprocess.Popen(SCANCODE_LOC + scan_command, stdout=subprocess.PIPE, shell=True)
            out, err = process.communicate()
        if err:
            return_results(infos, 'ERROR')
        else:
            return_results(infos, 'FINISHED', working_dir)
    except Exception, e:
        decrease_current_count_by_one()
        change_status_in_db('NOT STARTED', infos['location'])
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_msg = str(exc_type.__name__) + ' at line "' + str(exc_traceback.tb_lineno) + '" in "' + __file__ + '"'
        write_log(str(error_msg))


if __name__ == '__main__':
    import sys
    input_file = sys.argv[1]
    scan_in_sub_process(input_file)
