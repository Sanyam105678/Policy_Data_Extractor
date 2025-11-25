from django.urls import path
from . import views

urlpatterns = [
   
    path("upload/", views.upload_policy, name="upload_policy"),
    
    path("ocr-logs/download/<path:filename>/", views.download_log, name="download_log"),  
]