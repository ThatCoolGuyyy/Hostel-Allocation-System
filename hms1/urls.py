"""hms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from app import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'message', views.MessageView, 'msg')

urlpatterns = [
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('', views.home, name='index'),
    path('signup/student', views.index, name='index'),
    path('login/student', views.st_login, name='index'),
    path('signup/admin', views.admin_index, name='index'),
    path('login/admin', views.adm_login, name='index'),
    path('adm/home', views.adm_home, name='index'),
    path('st/home', views.st_home, name='index'),
    path('api/student', views.C_student, name='index'),
    path('api/adm_update', views.U_admin, name='index'),
    path('st/st_update', views.U_student, name='index'),
    path('adm/profile', views.adm_profile, name='index'),
    path('adm/al_student', views.adm_al_st, name='index'),
    path('app/', include(router.urls)),
    path('st/profile', views.st_profile, name='index'),
    path('st/hall', views.st_hall, name='index'),
    path('adm/student', views.adm_st, name='index'),
    path('api/st_choose_hall', views.st_choose_hall, name='index'),
    path('api/adm_approve_st', views.adm_approve_st, name='index'),
    path('api/adm_login', views.L_admin, name='index'),
    path('api/st_logout', views.LO_student, name='index'),
    path('api/adm_logout', views.LO_admin, name='index'),
    path('404', views.p404, name='index'),
    path('404!', views.p405, name='index'),
    path('api/st_login', views.L_student, name='index'),
    path('api/admin', views.C_admin, name='admin'),
    path('admin/', admin.site.urls),
    path('st/api/msgg', views.msgg, name='msgg'),
    path('st/api/msgg1', views.msgg1, name='msgg1'),
]
