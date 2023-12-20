"""
URL configuration for FIS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('view_teacher/<int:teacher_id>', views.view_teacher, name='view_teacher'),
    path('update_teacher/<int:teacher_id>', views.update_teacher, name='update_teacher'),
    path('teacher/<int:teacher_id>',views.teacher_dashboard, name='teacher_dashboard'),
    path('adminfis/<int:admin_id>', views.admin_home, name='admin_home'),
    path('add_faculty/<int:admin_id>', views.add_faculty, name='add_faculty'),
    path('manage_faculty/', views.manage_faculty, name='manage_faculty'),
    path('update_faculty/<int:faculty_id>',views.update_faculty, name='update_faculty'),
    path('delete_faculty/<int:faculty_id>',views.delete_faculty, name='delete_faculty'),
    path('search_faculty/', views.search_faculty, name='search_faculty'),
    path('reports/', views.report_view, name='report_generation'),





]
