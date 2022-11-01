from knox import views as knox_views
from django.urls import path
from myapp.views import *
from .views import login as log
from myapp.api import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # non-api urls for views.py
    path('', home, name='home'),
    path('login/', log, name='login'),
    path('signup/', signup, name='signup'),
    path('loggedin/', loghome, name='loghome'),
    path('logout/', signout, name='logout'),
    path('tasks/', tasks, name='tasks'),
    path('adminlogin/', adminlogin, name="adminlogin"),
    path('adminhome/', adminhome, name="adminhome"),
    path('addapp/', addapp, name='addapp'),
    path('addimage/<int:id>', addimage, name='addimage'),
    # api-endpoint urls pointed to api.py
    path('api/getapp/<int:id>/', getapps, name='getappapi'),
    path('api/register/', RegisterAPI.as_view(), name='registerationapi'),
    path('api/login/', LoginAPI.as_view(), name='loginapi'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logoutapi'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutallapi'),
    path('api/user/', userops.as_view(), name='userops'),
    path('api/admin/', adminops.as_view(), name="admintaskview")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
