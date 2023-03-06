from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="project_3_mail/index"),
    path("login", views.login_view, name="project_3_mail/login"),
    path("logout", views.logout_view, name="project_3_mail/logout"),
    path("register", views.register, name="project_3_mail/register"),

    # API Routes
    path("emails", views.compose, name="project_3_mail/compose"),
    path("emails/<int:email_id>", views.email, name="project_3_mail/email"),
    path("emails/<str:mailbox>", views.mailbox, name="project_3_mail/mailbox"),
]
