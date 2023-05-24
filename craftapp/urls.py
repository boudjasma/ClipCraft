from django.urls import path
from craftapp.views import HomeView, CustomLoginView, CustomLogoutView, SignUpView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(template_name = 'craftapp/logout.html'), name='logout'),
    path('signup/', SignUpView.as_view(template_name = 'craftapp/signup.html'), name='signup'),
    path('accounts/profile/', HomeView.as_view(template_name="craftapp/home.html"), name="home"),
] 