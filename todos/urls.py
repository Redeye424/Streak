"""
URL configuration for todos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from todo1 import views
urlpatterns = [
    path('', views.home, name='home'),

    path("accounts/signup/", views.signup, name="signup"),
    path("about_us", views.about_us, name="about_us"),

    path("accounts/login/", views.CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", views.accounts, name="logout"),

    path('make_streak/', views.create_streak, name='create_streak'),

    path("accounts/", include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
]
