from django.conf.urls import url
from . import views



app_name = 'common'
urlpatterns = [
   
    url(r'^$', views.homepage_subscription),

]
