from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from expenses import views

urlpatterns = [
    path('', lambda request: redirect('/login/')),
    path('admin/', admin.site.urls),

    path('', include('django.contrib.auth.urls')),

    path('signup/', views.signup, name='signup'),
    path('expenses/', include('expenses.urls')),
]