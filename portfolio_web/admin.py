from django.contrib import admin
from .models import Project, Skill, Experience, ContactMessage, Education, Certificate, Resume
# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "sort_order", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "tech_stack")
    list_filter = ("is_featured",)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "sort_order")
    search_fields = ("name", "category")

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "organization", "is_current", "start_date", "end_date", "sort_order")
    search_fields = ("role", "organization")
    list_filter = ("is_current",)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "start_year", "end_year", "gpa")
    search_fields = ("end_year", "institution")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "issued_date", "credential_url", "sort_order")
    search_fields = ("title", "issuer", "credential_url")


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    search_fields = ("title",)