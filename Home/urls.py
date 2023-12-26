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
    path('update_faculty_idv/<int:faculty_id>',views.update_faculty_idv, name='update_faculty_idv'),
    path('add_work_exp_details/<int:faculty_id>', views.add_work_exp_details, name='add_work_exp_details'),
    path('add_paper_details/<int:faculty_id>',views.add_paper_details, name='add_paper_details'),
    path('add_patent_details/<int:faculty_id>', views.add_patent_details, name='add_patent_details'),
    path('add_certificate_details/<int:faculty_id>', views.add_certificate_details, name='add_certificate_details'),
    path('add_education_details/<int:faculty_id>', views.add_education_details, name='add_education_details'),
    path('add_conference_details/<int:faculty_id>', views.add_conference_details, name='add_conference_details'),
    path('add_faculty_details/<int:faculty_id>',views.add_faculty_details, name='add_faculty_details'),
    path('reports_gender_1/', views.report_view_gender, name='report_generation_gender'),
    path('update_paper_idv/<int:faculty_id>/<int:paper_id>', views.update_paper_idv, name='update_paper_idv'),
    path('update_patent_idv/<int:faculty_id>/<int:patent_id>',views.update_patent_idv, name='update_patent_idv'),
    path('update_conference_idv/<int:faculty_id>/<int:conference_id>', views.update_conference_idv, name='update_conference_idv'),
    path('update_certificate_idv/<int:faculty_id>/<int:certificate_id>', views.update_certificate_idv, name='update_certificate_idv'),
    path('update_education_details_idv/<int:faculty_id>/<int:education_details_id>', views.update_education_details_idv, name='update_education_details_idv'),
    path('update_work_exp_idv/<int:faculty_id>/<int:work_exp_id>',views.update_work_exp_idv, name='update_work_exp_idv'),
    path('delete_paper_idv/<int:faculty_id>/<int:paper_id>', views.delete_paper_idv, name='delete_paper_idv'),
    path('delete_patent_idv/<int:faculty_id>/<int:patent_id>', views.delete_patent_idv, name='delete_patent_idv'),
    path('delete_conference_idv/<int:faculty_id>/<int:conference_id>', views.delete_conference_idv, name='delete_conference_idv'),
    path('delete_certificate_idv/<int:faculty_id>/<int:certificate_id>', views.delete_certificate_idv, name='delete_certificate_idv'),
    path('delete_education_details_idv/<int:faculty_id>/<int:education_details_id>', views.delete_education_details_idv, name='delete_education_details_idv'),
    path('delete_work_exp_idv/<int:faculty_id>/<int:work_exp_id>', views.delete_work_exp_idv, name='delete_work_exp_idv'),
    path('report_conference_1/', views.conference_join_report, name="conference_join_report"),
    path('report_department_1/', views.department_join_report,name="department_join_report"),
    path('report_generation/', views.report_generation, name='report_generation'),

]
