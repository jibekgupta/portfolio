from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    intro_blurb = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=300, blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)

    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Skill(models.Model):
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=120, blank=True)
    level = models.CharField(max_length=50, blank=True)
    sort_order = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name
    


class Experience(models.Model):
    role = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)  # blank if current
    is_current = models.BooleanField(default=False)

    description = models.TextField(help_text="Use bullet-like lines, one per line.", blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.role} — {self.organization}"



class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field = models.CharField(max_length=200, blank=True)

    start_year = models.DateField(null=True, blank=True)
    end_year = models.DateField(null=True, blank=True)  # blank if current
    gpa = models.CharField(max_length=20, blank=True)
    focus = models.TextField(help_text="Use comma-separated values.", blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', '-end_year']
    
    def __str__(self):
        return f"{self.degree} — {self.institution}"