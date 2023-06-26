import datetime
from typing import Any, Dict
from django.shortcuts import redirect, render
from django.views.generic import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
import requests
from .forms import SignUpForm
from .models import Profile, Video, VideoFeedback
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.paginator import Paginator

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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'craftapp/profile.html'
    paginate_by = 3  # Nombre de vidéos par page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        videos = self.request.user.profile.videos.all()  # Récupère les vidéos du profil de l'utilisateur connecté

        paginator = Paginator(videos, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context

    def post(self, request):
        profile = request.user.profile
        if request.method == 'POST':
            if request.POST.get('description') is not None :
                description = request.POST.get('description')
                profile.description = description
                profile.save()

            if request.FILES.get('file') is not None :
                picture=request.FILES.get('file')
                profile.picture=picture
                profile.save()

        return render(request, self.template_name)
      

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'craftapp/home.html'
    
    # def get(self, request, format=None):
    #     return JsonResponse({"message":'HELLO WORLD FROM DJANGO AND DOCKER'})  

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["avatars"] = ["{% static 'assets/avatar"+str(i)+".png' %}" for i in range(1, 8)]
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
            url_api = "http://192.168.1.64:5000/generate-video"
            # "https://clipcraftapi-quimarche-bvid2oohxq-lz.a.run.app/generate-video"
            # 'http://35.195.149.150:5000/generate-video'
            response = requests.post(url_api, data=data)
            print(response)
            if response.status_code == 200:
                data = response.json()
                url = data["video_url"]
                title_video = title_video
                video = Video.objects.create(title=title_video, text=text, avatar="media/static/assets/"+photo+".png", url=url)
                profile = request.user.profile
                profile.videos.add(video)
                profile.save()
                
                context = {
                    'title': title_video,
                    'text': text,
                    'photo': photo,
                    'video_path': url,
                }

                return render(request, 'craftapp/result.html', context)
            else:
                return HttpResponse('Error occurred during video generation.', status=response.status_code)

class ResultView(LoginRequiredMixin, TemplateView):
    template_name = 'craftapp/result.html'

class FeedbackView(LoginRequiredMixin, TemplateView):
    template_name = 'craftapp/feedback.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["video"] = self.request.user.profile.videos.latest('uploaded_at')
        context["range"] = range(1, 11)
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            evaluation = int(request.POST.get('mark'))
            last_video = request.user.profile.videos.latest('uploaded_at')
            last_video.evaluation = evaluation
            last_video.save()
            feedback_video= VideoFeedback.objects.create(video=last_video, mark=evaluation)
            print(feedback_video.video, feedback_video.mark)

        return render(request, 'craftapp/home.html')
      