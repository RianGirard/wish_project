from django.shortcuts import render, redirect
import bcrypt, re
from .models import User, Wish
from django.contrib import messages
from django.utils import timezone

def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        if len(User.objects.filter(email=request.POST['email'])) == 0:
            messages.error(request, "Please enter a valid email and password")
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])[0]
        if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
            request.session['user_id'] = this_user.id
            return redirect('/success')
        messages.error(request, "Please enter a valid email and password")
    return redirect('/')


def register(request):
    errors = User.objects.user_validator(request.POST)
    # if len(errors) > 0:
    if errors:                                  # more concise to just say "if errors", as opposed to measuring its length
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    elif request.method == "POST":
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            fname=request.POST['first_name'],
            lname=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash
        )
        request.session['user_id']= new_user.id
        # could add here ~  messages.success(request, "whatever")
        return redirect('/success')
    return redirect('/')


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return redirect('/wishes')

# -------------------------------------------------------------------------------------------------
# AJAX validators: 

def email_valid_null(request):
    # this is here to deal with null text entry cases
    found = 3
    return render(request, 'partials/email.html', {"found":found})

def email_valid(request, email):
    list = User.objects.filter(email=email)
    found = 2
    if len(list) > 0:
        found = 1
    return render(request, 'partials/email.html', {"found":found})      # found must be a dict datatype

def email_regex_null(request):
    # this is here to deal with null text entry cases
    found = 6
    return render(request, 'partials/email.html', {"found":found})

def email_regex(request, email):
    found = 4
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if EMAIL_REGEX.match(email):
        found = 5
    return render(request, 'partials/email.html', {"found":found})      # found must be a dict datatype
# ----------------------------------------------------------------------------------------------------

def wishes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "this_user" : User.objects.get(id=request.session['user_id']),
        "all_wishes" : Wish.objects.all(),
    }
    return render(request, 'wishes.html', context)

def wishes_new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
    }
    return render(request, "new_wish.html", context)

def create_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        Wish.objects.create(item=request.POST['item'], desc=request.POST['description'], user=user)
    return redirect('/wishes')

def destroy_wish(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=id)
    wish.delete()
    return redirect('/wishes')

def wish_edit(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "this_user" : User.objects.get(id=request.session['user_id']),
        "wish" : Wish.objects.get(id=id),
    }
    return render(request, 'wish_edit.html', context)

def update_wish(request): 
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        wish = Wish.objects.get(id=request.POST['wish_id'])
        wish.item=request.POST['item']
        wish.desc=request.POST['description']
        wish.save()
    return redirect('/wishes')

def grant_wish(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=id)
    now = timezone.now()
    wish.granted=True
    wish.granted_at=now
    wish.save()
    return redirect('/wishes')

def like_wish(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    wish = Wish.objects.get(id=id)
    wish.users_who_like.add(user)
    return redirect('/wishes')

def stats(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    all_wishes_granted = Wish.objects.filter(granted=True)
    granted = Wish.objects.filter(granted=True).filter(user=user)
    not_granted = Wish.objects.filter(granted=False).filter(user=user)


    context = {
        "this_user" : User.objects.get(id=request.session['user_id']),
        "all_wishes_granted" : all_wishes_granted,
        "granted" : granted,
        "not_granted" : not_granted,
    }
    return render(request, 'stats.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


# Create your views here.
