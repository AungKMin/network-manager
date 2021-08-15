from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import ContactPointForm, CreateUserForm, ContactForm
from .filters import ContactPointFilter, ContactFilter
from .decorators import unauthenticated_user

from itertools import chain

"""
Home
"""
@login_required(login_url='login') # restrict access to page (require user to be logged in)
def home(request):
    user_wrapper = UserWrapper.objects.get(user__username=request.user.username)

    contacts = user_wrapper.contact_set.all() # get all contacts associated with user

    # get all contact points for all contacts of the user
    contact_points = ContactPoint.objects.none()
    for contact in contacts:
        contact_points = contact_points | contact.contactpoint_set.all()

    total_contacts = contacts.count() # count number of contacts
    total_contact_points = contact_points.count() # count number of contact points

    sent = contact_points.filter(status='Sent').count() # number of contact points that are sent
    responded = contact_points.filter(status='Responded - reply').count() # number of contact points where the contact has responded

    contact_filter = ContactFilter(request.GET, queryset=contacts) #create filter for search
    contacts = contact_filter.qs #set contacts displayed to the filtered queryset

    user_wrapper = UserWrapper.objects.get(user__username=request.user.username) # get user_wrapper for current logged-in user
    contact_filter.form.fields["contact_tags"].queryset = user_wrapper.contacttag_set # limit possible contact tags to only the ones belonging to the user 

    contact_points = contact_points.order_by('-date_created')[:5] # send only the latest five contact points

    context = {'contact_points': contact_points, 'contacts': contacts, 
    'total_contacts': total_contacts, 'total_contact_points': total_contact_points,
    'sent': sent, 'responded': responded, 
    'contact_filter': contact_filter}

    return render(request, 'accounts/dashboard.html', context)


"""
Contact Point Method Page
"""
@login_required(login_url='login') # restrict access to page (require user to be logged in)
def contact_point_methods(request):


    user_wrapper = UserWrapper.objects.get(user__username=request.user.username) # get user_wrapper for current logged-in user
    contact_point_methods = user_wrapper.contactpointmethod_set.all() # limit possible contact point methods to only the ones belonging to the user 

    return render(request, 'accounts/contact_point_methods.html', {'contact_point_methods': contact_point_methods})


"""
Contact Page
"""
@login_required(login_url='login') # restrict access to page (require user to be logged in)
def contact(request, pk):
    
    contact = Contact.objects.get(id=pk) # get requested contact

    contact_points = contact.contactpoint_set.all() # get all contact points for this contact
    # calculate number of times contact has been contacted
    times_contacted = 0
    for contact_point in contact_points:
        times_contacted += contact_point.times_used

    contact_point_filter = ContactPointFilter(request.GET, queryset=contact_points) #create filter for search
    contact_points = contact_point_filter.qs #set contact points displayed to the filtered queryset

    context = {'contact': contact, 'contact_points': contact_points, 'times_contacted': times_contacted, 'contact_point_filter': contact_point_filter}
    return render(request, 'accounts/contact.html', context)

"""
Contact Settings Page - Update
"""
@login_required(login_url="login")
def contact_settings(request, pk):

    contact = Contact.objects.get(id=pk) # get referenced contact
    form = ContactForm(instance=contact) # make form to edit contact

    user_wrapper = UserWrapper.objects.get(user__username=request.user.username) # get user_wrapper for current logged-in user
    form.fields["contact_tags"].queryset = user_wrapper.contacttag_set # limit possible contact tags to only the ones belonging to the user 

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact) # create form with form data to submit
        if form.is_valid():
            form.save()

    context = {'contact': contact, 'form': form}
    return render(request, 'accounts/contact_settings.html', context=context)

"""
Contact Settings Page - Create
"""
@login_required(login_url="login")
def create_contact(request):

    form = ContactForm() # make form for creating contact

    user_wrapper = UserWrapper.objects.get(user__username=request.user.username) # get user_wrapper for current logged-in user
    form.fields["contact_tags"].queryset = user_wrapper.contacttag_set # limit possible contact tags to only the ones belonging to the user 

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES) # create form with form data to submit
        if form.is_valid():
            contact = form.save() # save contact to database

            # get UserWrapper for current user
            user_wrapper = UserWrapper.objects.get(user__username=request.user.username)
            contact.user_wrapper = user_wrapper # set newly-created contact's UserWrapper to current user
            contact.save()

            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/contact_settings.html', context=context)


"""
Form to create a contact point (handles get and post request)
"""
@login_required(login_url='login') # restrict access to page (require user to be logged in)
def create_contact_point(request, pk):

    ContactPointFormSet = inlineformset_factory(Contact, ContactPoint, fields=('contact_point_method', 'link', 'status', 'notes'), extra=2) # create formset template for creating multiple contact points
    contact = Contact.objects.get(id=pk) # get referenced contact
    formset = ContactPointFormSet(instance=contact) # create formset with desired contact
    #form = ContactPointForm(initial={'contact':contact}) # make form

    user_wrapper = UserWrapper.objects.get(user__username=request.user.username) # get user_wrapper for current logged-in user
    formset.forms[0].fields["contact_point_method"].queryset = user_wrapper.contactpointmethod_set # limit possible contact point methods to only the ones belonging to the user 

    if request.method == 'POST': # if the request is post, update the database with the form data
        #form = ContactPointForm(request.POST) # create a new contact point
        formset = ContactPointFormSet(request.POST, instance=contact) # create formset with form data to submit
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/contact_point_form.html', context)


"""
Form to update a contact point
"""
@login_required(login_url='login') # restrict access to page (require user to be logged in)
def update_contact_point(request, pk):

    contact_point = ContactPoint.objects.get(id=pk) # get requested contact point
    form = ContactPointForm(instance=contact_point) # set up form with the correct contact point

    user_wrapper = UserWrapper.objects.get(user__username=request.user.username) # get user_wrapper for current logged-in user
    form.fields["contact_point_method"].queryset = user_wrapper.contactpointmethod_set # limit possible contact point methods to only the ones belonging to the user 

    if request.method == 'POST': # if the request is post, update the database with the form data
        form = ContactPointForm(request.POST, instance=contact_point) # update the desired contact point
        if form.is_valid():
            form.save()
            return redirect('/') 

    context = {'form': form}
    return render(request, 'accounts/contact_point_form.html', context)


"""
Delete a contact point
"""
@login_required(login_url='login') # restrict access to page (require user to be logged in)
def delete_contact_point(request, pk):

    contact_point = ContactPoint.objects.get(id=pk) 
    if request.method == 'POST': 
        contact_point.delete()
        return redirect('/')

    context = {'item': contact_point}
    return render(request, 'accounts/delete.html', context)

"""
Create/Update contact tags
"""
@login_required(login_url='login') # restrict access to page (require user to be logged in)
def create_contact_tags(request): 
    ContactTagFormSet = inlineformset_factory(UserWrapper, ContactTag, fields='__all__', extra=5) # create formset template for creating multiple contact tags

    user_wrapper = UserWrapper.objects.get(user__username=request.user.username) # get referenced contact
    formset = ContactTagFormSet(instance=user_wrapper) # create formset with desired user

    if request.method == 'POST': # if the request is post, update the database with the form data
        formset = ContactTagFormSet(request.POST, instance=user_wrapper) # create formset with form data to submit
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/contact_point_form.html', context)

"""
Create/Update contact point methods
"""
@login_required(login_url='login') # restrict access to page (require user to be logged in)
def create_contact_point_methods(request): 
    ContactPointMethodFormSet = inlineformset_factory(UserWrapper, ContactPointMethod, fields='__all__', extra=5) # create formset template for creating multiple contact point methods
    user_wrapper = UserWrapper.objects.get(user__username=request.user.username) # get referenced contact
    formset = ContactPointMethodFormSet(instance=user_wrapper) # create formset with desired user

    if request.method == 'POST': # if the request is post, update the database with the form data
        formset = ContactPointMethodFormSet(request.POST, instance=user_wrapper) # create formset with form data to submit
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/contact_point_form.html', context)



"""
Registration Form
"""
@unauthenticated_user
def register_page(request):

    form = CreateUserForm() # create registration form

    if request.method == 'POST':
        form = CreateUserForm(request.POST) # create registration with form data
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username') # get username from form

            UserWrapper.objects.create(user=user) # create a userwrapper and assign one-to-one relationship

            messages.success(request, 'Account created for ' + username)
            return redirect('login') # redirect user to login page
            
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

"""
Login Form
"""
@unauthenticated_user
def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username') # get username from form data
        password = request.POST.get('password') # get password from form data

        user = authenticate(request, username=username, password=password) # try to log the user in 

        # if account exists, redirect user to home page
        if user is not None:
            login(request, user)
            return redirect('home')
        else: # if account does not exist, redirect to login page with error message
            messages.error(request, 'Incorrect username and password combination')
            return redirect('login')

    context = {}
    return render(request, 'accounts/login.html', context)

"""
Logout 
"""
def logout_user(request):
    logout(request)
    return redirect('login')
