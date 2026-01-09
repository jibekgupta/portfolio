from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),                 # 1) Introduction section (home)
    path("about/", views.about, name="about"),         # 2) About me
    path("projects/", views.projects, name="projects"),# 3) All projects page
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("skills/", views.skills, name="skills"),      # 4) Skills
    path("experience/", views.experience, name="experience"),  # 5) Experience
    path("contact/", views.contact, name="contact"),   # 6) Contact emails
    path("contact/success/", views.contact_success, name="contact_success"),
]
