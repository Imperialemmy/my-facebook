from django.urls import path, include
from .views import login, signup, home, watch

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
    path('watch/', watch, name='video'),
]