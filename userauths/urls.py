
from . import views
from django.urls import path
#from django.contrib.auth import views as auth_views

#app_name='userauths'
urlpatterns = [
    
    path("signup", views.registration,name='register'),
    path("signin", views.loginview,name='signin'),
    path("logout", views.logout,name='logout'),
    path("my_profile", views.my_profile,name='my_profile'),
    path("profile/<username>", views.friend_profile,name='friend_profile'),
    #path('admin/logout/', auth_views.LogoutView.as_view(), name='admin_logout'),
    
    
]
