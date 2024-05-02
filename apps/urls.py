from django.conf.urls.i18n import i18n_patterns
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import path

from apps.views import BlogDetailDetailView, LoginView
from root import settings
from . import views


def send_email_to_user(request):
    email = request.GET.get('email')
    send_mail('Hello', 'Hello', settings.EMAIL_HOST_USER, [email])
    return HttpResponse('sucessfully send')


urlpatterns =[
    # path('', BlogTemplateView.as_view(), name='blog_page'),
    path('details/<uuid:pk>', BlogDetailDetailView.as_view(), name='blog_detail'),
    path('send-email', send_email_to_user)
]

# ------------- email verification ---------
urlpatterns += [
    path('signup/', views.signup, name='signup'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account_activation_complete/', views.account_activation_complete, name='account_activation_complete'),
    path('accounts/login/', LoginView.as_view(), name='login'),  # Add this line for login
]
