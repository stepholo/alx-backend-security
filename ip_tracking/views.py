from django.shortcuts import render
from ratelimit.decorators import ratelimit


@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    """View to handle user login with rate limiting."""
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, 'login.html')

# Create your views here.
