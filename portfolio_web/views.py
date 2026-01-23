from __future__ import annotations

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
import logging

from .models import Project, Skill, Experience, Education, Certificate, Resume
from .forms import ContactForm

log = logging.getLogger(__name__)


def _has_field(model, field_name: str) -> bool:
    return field_name in {f.name for f in model._meta.get_fields()}


def _project_queryset(limit: int | None = None):
    """
    Return a robust Project queryset that works with either:
      - is_featured(bool) or featured(bool)
      - sort_order(int) optional
      - created_at(DateTime) optional
    """
    qs = Project.objects.all()

    # Prefer explicit featured flags if present
    if _has_field(Project, "is_featured"):
        qs = qs.filter(is_featured=True)
    elif _has_field(Project, "featured"):
        qs = qs.filter(featured=True)

    order_by = []
    if _has_field(Project, "sort_order"):
        order_by.append("sort_order")
    # Keep most-recent next if present
    if _has_field(Project, "created_at"):
        order_by.append("-created_at")

    if not order_by:
        # Fallback deterministic order
        order_by.append("title")

    qs = qs.order_by(*order_by)
    return qs[:limit] if limit else qs


def _skills_grouped():
    """
    Build skill sections grouped by category if choices exist.
    Falls back to a simple list if categories are missing.
    """
    skills_qs = Skill.objects.all()
    if _has_field(Skill, "sort_order"):
        skills_qs = skills_qs.order_by("sort_order", "name")
    else:
        skills_qs = skills_qs.order_by("name")

    # Group only if a 'category' field exists
    if _has_field(Skill, "category"):
        # Code -> Label map if choices defined
        try:
            choices = dict(Skill._meta.get_field("category").choices)
        except Exception:
            choices = {}

        buckets = {}
        for s in skills_qs:
            key = getattr(s, "category", "") or "Other"
            buckets.setdefault(key, []).append(s)

        # Order: PL, FW, TT, SP if present; then others alphabetically
        preferred = ["PL", "FW", "TT", "SP"]
        ordered_keys = [k for k in preferred if k in buckets] + [
            k for k in sorted(buckets.keys()) if k not in preferred
        ]

        sections = []
        for key in ordered_keys:
            label = choices.get(key, key)
            sections.append((label, buckets[key]))
        return sections

    # No category field → single unlabeled section
    return [("Skills", list(skills_qs))]


def _experiences_qs():
    qs = Experience.objects.all()
    order = []
    if _has_field(Experience, "sort_order"):
        order.append("sort_order")
    if _has_field(Experience, "is_current"):
        order.append("-is_current")
    if _has_field(Experience, "start_date"):
        order.append("-start_date")
    return qs.order_by(*order) if order else qs.order_by("title")


def _education_qs():
    qs = Education.objects.all()
    order = []
    if _has_field(Education, "sort_order"):
        order.append("sort_order")
    if _has_field(Education, "start_date"):
        order.append("-start_date")
    return qs.order_by(*order) if order else qs.order_by("degree")


def _certificates_qs():
    qs = Certificate.objects.all()
    order = []
    if _has_field(Certificate, "sort_order"):
        order.append("sort_order")
    if _has_field(Certificate, "issued_date"):
        order.append("-issued_date")
    return qs.order_by(*order) if order else qs.order_by("title")


def _latest_resume():
    return Resume.objects.order_by("-updated_at").first()


# ---------- Single-page Home (sections: hero, about, resume, projects, contact) ----------
def home(request):
    """
    Renders the single-page portfolio and also handles the contact form submission.
    """
    # Contact form (POST to same URL)
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        msg = form.save()

        # Prepare an email (optional) — won’t crash if email isn’t configured.
        recipient = getattr(settings, "PORTFOLIO_CONTACT_TO_EMAIL", None)
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
            settings, "SERVER_EMAIL", "no-reply@localhost"
        )

        if recipient:
            subject = f"[Portfolio] {msg.subject or 'New message'}"
            body = (
                f"New contact message from your portfolio:\n\n"
                f"Name: {msg.name}\n"
                f"Email: {msg.email}\n"
                f"Subject: {msg.subject}\n\n"
                f"Message:\n{msg.message}\n\n"
                f"Sent at: {msg.created_at}\n"
            )
            try:
                EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=from_email,
                    to=[recipient],
                    reply_to=[msg.email],
                ).send(fail_silently=False)
            except Exception:
                log.exception("Failed to send contact email")

        # On success, redirect back to the contact section anchor
        return redirect("/#contact")

    context = {
        # Sections
        "skills_sections": _skills_grouped(),
        "experiences": _experiences_qs(),
        "education": _education_qs(),
        "certificates": _certificates_qs(),
        "projects": _project_queryset(limit=6),  # show 6 cards on the page
        "resume": _latest_resume(),
        # Contact form
        "form": form,
    }
    return render(request, "portfolio_web/home.html", context)


# ---------- (Optional) Keep these routes if you still link to them ----------
def about(request):
    return render(request, "portfolio_web/about.html")


def projects(request):
    # Full projects page if you decide to keep it
    qs = _project_queryset(limit=None)
    return render(request, "portfolio_web/projects.html", {"projects": qs})


def project_detail(request, slug):
    # Supports both slug-based and pk-based detail depending on your URL config
    lookup = {"slug": slug} if _has_field(Project, "slug") else {"pk": slug}
    project = get_object_or_404(Project, **lookup)
    return render(request, "portfolio_web/project_detail.html", {"project": project})


def skills(request):
    return render(request, "portfolio_web/skills.html", {"skills": Skill.objects.all()})


def experience(request):
    return render(request, "portfolio_web/experience.html", {"experience": _experiences_qs()})


def contact(request):
    """
    Separate contact page route (kept for compatibility).
    Your single-page home already handles the form; this remains if you have a nav link.
    """
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        msg = form.save()
        recipient = getattr(settings, "PORTFOLIO_CONTACT_TO_EMAIL", None)
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
            settings, "SERVER_EMAIL", "no-reply@localhost"
        )
        if recipient:
            try:
                EmailMessage(
                    subject=f"[Portfolio] {msg.subject or 'New message'}",
                    body=f"{msg.name} <{msg.email}>\n\n{msg.message}",
                    from_email=from_email,
                    to=[recipient],
                    reply_to=[msg.email],
                ).send(fail_silently=False)
            except Exception:
                log.exception("Failed to send contact email")

        return redirect("contact_success")

    return render(request, "portfolio_web/contact.html", {"form": form})


def contact_success(request):
    return render(request, "portfolio_web/contact_success.html")
