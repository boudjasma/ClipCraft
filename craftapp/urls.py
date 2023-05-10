from django.urls import path
from craftapp.views import HomeView, CustomLoginView, CustomLogoutView, SignUpView
from django.conf.urls import include, url

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(template_name = 'craftapp/logout.html'), name='logout'),
    path('signup/', SignUpView.as_view(template_name = 'craftapp/signup.html'), name='signup'),
    path('accounts/profile/', HomeView.as_view(template_name="craftapp/home.html"), name="home"),
] 