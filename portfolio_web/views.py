from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Skill, Experience, Education
from .forms import ContactForm
import logging
from django.core.mail import EmailMessage
from django.conf import settings


# Create your views here.
def home(request):
    featured_projects = (
        Project.objects.filter(is_featured=True)
        .order_by("sort_order", "-created_at")[:6]
    )
    education = Education.objects.all()[:1]
    return render(request, "portfolio_web/home.html", {"featured_projects": featured_projects,
                                                       "education": education})


def about(request):
    return render(request, "portfolio_web/about.html")


def projects(request):
    all_projects = Project.objects.order_by("sort_order", "-created_at")
    return render(request, "portfolio_web/projects.html", {"projects": all_projects})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "portfolio_web/project_detail.html", {"project": project})


def skills(request):
    # Order primarily by the numeric `sort_order` so items appear 1, 2, 3...
    # then fall back to the name for a deterministic tie-breaker.
    all_skills = Skill.objects.order_by("sort_order", "name")
    return render(request, "portfolio_web/skills.html", {"skills": all_skills})


def experience(request):
    items = Experience.objects.order_by("sort_order", "-is_current", "-start_date")
    return render(request, "portfolio_web/experience.html", {"experience": items})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            
            subject = f"[Portfolio] {msg.subject or 'New message'}"
            body = (
                f"New contact message from your portfolio:\n\n"
                f"Name: {msg.name}\n"
                f"Email: {msg.email}\n"
                f"Subject: {msg.subject}\n\n"
                f"Message:\n{msg.message}\n\n"
                f"Sent at: {msg.created_at}\n"
            )

            # Prepare email safely — make sending optional so the site
            # doesn't crash when no email settings exist (useful for dev).
            recipient = getattr(settings, "PORTFOLIO_CONTACT_TO_EMAIL", None)
            # Prefer DEFAULT_FROM_EMAIL, fall back to SERVER_EMAIL, then a no-reply address.
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "SERVER_EMAIL", "no-reply@localhost")

            if recipient:
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=from_email,
                    to=[recipient],
                    reply_to=[msg.email],
                )

                try:
                    email.send(fail_silently=False)
                except Exception:
                    # Log the failure but don't prevent the user from seeing success.
                    logging.getLogger(__name__).exception("Failed to send contact email")

            return redirect("contact_success")
    else:
        form = ContactForm()
    return render(request, "portfolio_web/contact.html", {"form": form})


def contact_success(request):
    return render(request, "portfolio_web/contact_success.html")
