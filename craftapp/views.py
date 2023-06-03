import datetime
from typing import Any, Dict
from django.shortcuts import redirect, render
from django.views.generic import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
import requests
from .forms import SignUpForm
from .models import Profile, Video
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse

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

            Profile.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
            )

            user = authenticate(username=user.username, password=password)
            login(request, user)

            return redirect('home')
        else:
            print(form.errors)

        return render(request, self.template_name, {'form': form})
    

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'craftapp/home.html'
    
    # def get(self, request, format=None):
    #     return JsonResponse({"message":'HELLO WORLD FROM DJANGO AND DOCKER'})  

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

            title_video = request.user.username+"-"+title.replace(" ","-")+"-"+str(datetime.datetime.now()).replace(" ","-")
          
            data = {
                'title': title_video,
                'text': text,
                'photo': photo
            }
            print(data)

            response = requests.post('http://127.0.0.1:5000/generate-video', data=data)

            if response.status_code == 200:
                url_video = response.json()
                title_video = title_video
                video = Video.objects.create(title=title_video, url=url_video)
                profile = request.user.profile
                profile.videos.add(video)
                profile.save()
                
                context = {
                    'title': title_video,
                    'text': text,
                    'photo': photo,
                    'video_path': "url_video"
                }

                return render(request, 'craftapp/result.html', context)
            else:
                return HttpResponse('Error occurred during video generation.', status=response.status_code)