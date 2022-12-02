"""task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from webapp.views import TodoView, View, TodoCreate, UpdateTodo, Delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TodoView.as_view(), name="index"),
    path('todo/<int:pk>/', View.as_view(), name="view"),
    path('todo/create/', TodoCreate.as_view(), name="create"),
    path('todo/<int:pk>/update/', UpdateTodo.as_view(), name="update"),
    path('todo/<int:pk>/delete/', Delete.as_view(), name='delete'),
]
