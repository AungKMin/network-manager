from django.http import HttpResponse
from django.shortcuts import redirect

"""
decorator to redirect unathenticated users to login page
"""
def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated: 
            return redirect('home')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function