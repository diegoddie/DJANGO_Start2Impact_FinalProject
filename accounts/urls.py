from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html",authentication_form=LoginForm), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html', email_template_name='password_reset_email.html', success_url=reverse_lazy('accounts:password_reset_done')), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html',success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)