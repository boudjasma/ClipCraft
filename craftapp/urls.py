from django.urls import path
from craftapp.views import HomeView, CustomLoginView, CustomLogoutView, SignUpView, ProfileView, ResultView, FeedbackView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(template_name = 'craftapp/logout.html'), name='logout'),
    path('signup/', SignUpView.as_view(template_name = 'craftapp/signup.html'), name='signup'),
    path('accounts/profile/', HomeView.as_view(template_name="craftapp/home.html"), name="home"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('result/', ResultView.as_view(), name="result"),
    path('feedback/', FeedbackView.as_view(), name="feedback")
    
] 