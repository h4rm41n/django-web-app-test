"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from peserta import views

urlpatterns = [
    path('', views.Dashboard.as_view()),
    path('kontrol/', admin.site.urls),
    path('input/', views.formInput),
    path('delete/<int:id>', views.deleteData),

    path('programlist', views.ListProgram.as_view(), name='list-program'),
    path('programnew', views.CreateProgram.as_view(), name='new-program'),
    path('programedit/<int:pk>', views.EditProgram.as_view(), name='edit-program'),
    # path('programdelete', views.DeleteProgram.as_view(), name='delete-program')
    path('programdelete/<int:id>', views.DeleteProgram.as_view(), name='delete-program')
]
