from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from expenses import views

urlpatterns = [
    path('', lambda request: redirect('/login/')),
    path('admin/', admin.site.urls),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('signup/', views.signup, name='signup'),
    path('expenses/', include('expenses.urls')),
]