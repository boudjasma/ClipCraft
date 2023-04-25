from django.urls import path
from craftapp.views import HomeView

urlpatterns = [
    path('', HomeView.as_view()),
]