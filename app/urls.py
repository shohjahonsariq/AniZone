from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import GoogleAutoLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('anime/<int:pk>/', views.anime_detail, name='anime_detail'),
    path('episode/<int:pk>/', views.episode_detail, name='episode_detail'),
    path('profile/', login_required(views.profile), name='profile'), 
    path('google-auto-login/', GoogleAutoLoginView.as_view(), name='google_auto_login'),
    path('anime/<int:pk>/like/', views.like_anime, name='like_anime'),
]
