from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        requested_page = self.get_redirect_url()

        if requested_page:
            return requested_page

        return reverse_lazy('properties:property_list')