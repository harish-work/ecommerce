from django.urls import path
from .views import RegisterView,LoginView,UserDetailsView
urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    # path('<int:pk>/me', UserDetailsView.as_view(),name='details'),
    path('me/', UserDetailsView.as_view(),name='details'),

]