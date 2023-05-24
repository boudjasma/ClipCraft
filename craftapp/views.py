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

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            title = request.POST.get('title')
            text = request.POST.get('text')
            selected_photo = str(request.POST.get('photo'))
            print(title, text, selected_photo)
            # traitement de données se fait ici
            context = {'title': title, 'text': text, 'photo': selected_photo }
            
            # generate_video(text, selected_photo)

            # return render(request, 'craftapp/result.html', context)
            data = {
                'title': title,
                'text': text,
                'selected_photo': selected_photo
            }

            print(data)
            # Effectuez la requête POST vers votre API
            response = requests.post('http://localhost:5000/generate-video', data=data)

            # Traitez la réponse de l'API si nécessaire
            api_response = response.json()
            print(api_response)

            # Traitez les données et construisez le contexte
            context = {'title': title, 'text': text, 'selected_photo': selected_photo }

            # Renvoyez la réponse à la vue 'result.html'
            return render(request, 'craftapp/result.html', context)