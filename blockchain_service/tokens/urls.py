from django.urls import path

from .views import *

urlpatterns = [
    path('create/', TokenCreateAPIView.as_view()),
    path('list/', TokenListAPIView.as_view()),
]
