from django.urls import path

from .views import CreateAPIView

urlpatterns = [
    path('create/', CreateAPIView.as_view())
]
