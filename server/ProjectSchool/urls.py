"""ProjectSchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from timetable import views
from django.conf.urls.static import static

urlpatterns = [
    path('timetable/', include('timetable.urls')),
    path('admin/timetable/blok_timetable/add-real-data/', views.add_real_data, name="t_data"),
    path('admin/timetable/blok_timetable/test_data/', views.admin_geterate_test_data, name="admin_test_data"),
    path('admin/timetable/blok_timetable/gen-tt/', views.admin_geterate_test_data, ),
    path('admin/timetable/blok_timetable/clear/', views.delete_everything, name="del"),
    path('admin/timetable/blok_timetable/createTimeTable/', views.createTimeTable, 
         name="t_createTimeTable"),
    path('admin/', admin.site.urls),
    path('', include('timetable.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
