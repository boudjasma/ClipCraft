from django.shortcuts import redirect, render
from django.views.generic import *
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

class CustomLoginView(LoginView):
    template_name = 'craftapp/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'craftapp/logout.html'
    next_page = 'login'

class SignUpView(View):
    form_class = UserCreationForm
    template_name = 'craftapp/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user_created = User.objects.create_user(username=username, password=password, email=email)
            user_created.save()
            user = authenticate(username=username, password=password)
            
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})
    
class HomeView(TemplateView):
    template_name = 'craftapp/home.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            title = request.POST.get('title')
            text = request.POST.get('text')
            selected_photo = request.POST.get('photo')
            print(title, text, selected_photo)
            # traitement de données se fait ici
            context = {'title': title, 'text': text, 'selected_photo': selected_photo}
            
            return render(request, 'craftapp/result.html', context)



