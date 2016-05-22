from django.conf.urls import url
from views import index, upload, showscans

app_name = 'scanapp'

urlpatterns = [
        url(r'^$', index, name='index'),
        url(r'^upload$', upload, name='upload'),
        url(r'^showscans$', showscans, name='showscans')
    ]
