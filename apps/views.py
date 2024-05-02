from django.db.models import Q
from django.views.generic import ListView, DetailView

from apps.models import Category, Blog
from .tasks import send_activation_email


class BlogTemplateView(ListView):
    queryset = Blog.objects.all()
    template_name = 'blog-list-left-sidebar.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def get_queryset(self):

        search = self.request.GET.get('search')
        category_id = self.request.GET.get('category')
        queryset = super().get_queryset()
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class BlogDetailDetailView(DetailView):
    queryset = Blog.objects.all()
    template_name = 'blog-details-left-sidebar.html'


# ----------------------------------- Email verification 👇------------------------------------------------------

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CustomUser
from django.http import HttpResponseBadRequest

from .forms import CustomUserCreationForm
from .tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the user until email confirmation
            user.save()

            # Send email confirmation asynchronously
            current_site = get_current_site(request)
            send_activation_email.delay(user.id, current_site.domain)

            return redirect('account_activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and not user.activation_link_used and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.activation_link_used = True
        user.save()
        login(request, user)
        return redirect('account_activation_complete')
    else:
        return HttpResponseBadRequest('Activation link is invalid or has already been used!')


@login_required
def account_activation_complete(request):
    return render(request, 'account_activation_complete.html')


from django.contrib.auth.views import LoginView as BaseLoginView


class LoginView(BaseLoginView):
    template_name = 'registration/login.html'  # Specify your login template name

    def get_success_url(self):
        # Redirect users to a success page, or wherever you want
        return super().get_success_url()
