
from django.contrib import admin
from django.urls import path,include
from userauths import views
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/logout/', views.logout_view, name='admin_logout'),
    path("admin/", admin.site.urls),
    path("", include('core.urls')),
    path("user/", include('userauths.urls')),
   
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

