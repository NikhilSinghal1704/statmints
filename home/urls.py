from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('upload', views.upload, name = "upload_xlsx"),
    path('show/<what>', views.process, name = "process"),
    path('result', views.result, name = "result"),
]
