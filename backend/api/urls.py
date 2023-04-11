from django.urls import path, include
from processor import urls as processor_urls

urlpatterns = [
    path('processors/', include(processor_urls))
]
