from django.urls import reverse
from django.utils.http import urlencode

def get_reset_link(user):
    base_url = "https://localhost:4200"
    reset_path = reverse('password_reset_confirm')
    token = user.generate_reset_token()
    query_params = urlencode({'token': token})
    return f"{base_url}{reset_path}?{query_params}"