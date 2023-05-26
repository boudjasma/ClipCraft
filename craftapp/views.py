from typing import Any, Dict
from django.shortcuts import redirect, render
from django.views.generic import *
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
import requests
from .forms import SignUpForm
from .models import Profile


class CustomLoginView(LoginView):
    template_name = 'craftapp/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'craftapp/logout.html'
    next_page = 'login'

class SignUpView(View):
    form_class = SignUpForm
    template_name = 'craftapp/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()

            # Création du profil associé à l'utilisateur
            Profile.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
            )

            # Authentification et connexion de l'utilisateur
            user = authenticate(username=user.username, password=password)
            login(request, user)

            return redirect('home')
        else:
            # Afficher les erreurs du formulaire dans la console
            print(form.errors)

        return render(request, self.template_name, {'form': form})
    

class HomeView(TemplateView):
    template_name = 'craftapp/home.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["avatars"] = ["{% static 'assets/avatar"+str(i)+".png' %}" for i in range(1, 10)]
        print(context["avatars"] )
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            title = request.POST.get('title')
            text = request.POST.get('text')
            photo = str(request.POST.get('photo'))
          
            data = {
                'title': title,
                'text': text,
                'photo': photo
            }
            print(data)

            response = requests.post('http://localhost:5000/generate-video', data=data)

            api_response = response.json()
            print(api_response)

            context = {'title': title, 'text': text, 'photo': photo, 'video_path': api_response }

            # Renvoyez la réponse à la vue 'result.html'
            return render(request, 'craftapp/result.html', context)
        