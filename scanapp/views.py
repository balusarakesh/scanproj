from django.shortcuts import render
from models import Scanmodel
import subprocess
import os
from scan_helper import create_temp_directory
from scan_helper import get_random_chars
from scan_helper import shallow_extract_and_delete

def index(request):
    return render(request, 'scanapp/index.html')


def save_file(input_file):
    tmp_dir = create_temp_directory(get_random_chars())
    try:
        input_zip = os.path.join(tmp_dir, 'input.zip')
        with open(input_zip, 'wb+') as zip_file:
            for chunk in input_file.chunks():
                zip_file.write(chunk)
        shallow_extract_and_delete(input_zip)
        return tmp_dir
    except:
        print 'error'


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
def upload(request):
    email = request.POST.get('emailid')
    location = save_file(request.FILES['uploadedfile'])
    name = get_random_chars(10)
    url = 'https://s3-us-west-1.amazonaws.com/scansbucket/'  + name + '.zip'
    Scanmodel.objects.create(email=email, resultsurl=url, status='NOT STARTED', location=location)
    subprocess.Popen('python '+ os.path.join(CURRENT_DIR, 'scan_helper.py'), stdout=subprocess.PIPE, shell=True)
    context = {'download_URL' : url}
    return render(request, 'scanapp/scansurl.html', context)


def showscans(request):
    context = {'data': Scanmodel.objects.all()}
    return render(request,'scanapp/showscans.html', context)
