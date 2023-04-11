from django.urls import path
from .views import ProcessorListView

urlpatterns = [
    path('', ProcessorListView.as_view()),
]