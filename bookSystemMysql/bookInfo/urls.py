"""bookSystemMysql URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path('index/', views.index),  # 图书信息页面
    path('create/', views.create),  # 新增图书
    path("delete/<book_id>/", views.delete),  # 删除图书
    path('area/', views.get_areas),
    path('book/list/', views.book_json),
    path('login/', views.login),
    path('login_check/', views.login_check),
    path('test_ajax/', views.test_ajax),
    path('ajax_handler', views.ajax_handler),
    path("set_cookie/", views.set_cookie),
    path("get_cookie/", views.get_cookie),
    path("set_session/", views.set_session),
    path("get_session/", views.get_session)
]
