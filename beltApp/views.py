from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, UserManager, Show


# ________________________Render Routes ___________________________
def index(request):
    return render(request, 'index.html')


def dashboard(request):
    if "user_id" in request.session:
        new_user = User.objects.get(id=request.session["user_id"])
        context = {
            'user': new_user,
            'shows': Show.objects.all(),
            'users': User.objects.all(),
            # 'show': Show.objects.get(id=request.session["user_id"]),
        }
        return render(request, "dashboard.html", context)
    else:
        return redirect('/')


def new_page(request):
    context = {
        "shows": Show.objects.all(),
        "current_user": User.objects.get(id=request.session["user_id"])
    }
    # renders new.html page // link with Path in urls.py
    return render(request, 'new.html', context)


def edit_page(request, show_id):
    each_show = Show.objects.get(id=show_id)
    context = {
        "show": each_show,
        "this_user": User.objects.get(id=request.session["user_id"])

    }
    return render(request, "edit.html", context)


def show_page(request, show_id):
    show = Show.objects.get(id=show_id)
    context = {
        "show": show,
        "some_user": User.objects.get(id=request.session["user_id"])
    }
    return render(request, 'show.html', context)


# __________________________Action Routes___________________________

# ********************** Login and Registraion Logic
def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()  # create

        user = User()
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.password_hash = pw_hash
        user.save()
        request.session['user_id'] = User.objects.last().id
        return redirect("/dashboard")


def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            current_user = user[0]
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        request.session['user_id'] = current_user.id
    return redirect('/dashboard')


# MAKE SURE to clear the seesion or "/success" will fail and anyone can enter the Dashboard
def logout(request):
    del request.session['user_id']
    return redirect('/')
# ***************************** END Login and Registraion Logic

# ************************ Start Create Job Logic ************************


def create_show(request):
    # TO CREATE A NEW SHOW -- "show.objects.create(*** all the names from the FORM AREA ***)"
    # Make sure all variable names match Models Variable names.
    print("****************** H E L L O **********************")
    print(request.POST)
    if request.method == "POST":
        errors = Show.objects.validateShow(request.POST)
        print(errors, "?????????????????????")
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/shows/new')
        else:
            Show.objects.create(
                created_by=User.objects.get(id=request.session['user_id']),
                location=request.POST['location'],
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date'],
                description=request.POST['description'],
            )
        print(request.POST)
        # return redirect(f'/shows/{new_show.id}')
    return redirect('/dashboard')

# *************************** Update Job Listing Logic ********************


def updateShowDB(request, show_id):
    # DONT FORGET IF STATEMENT since we are UPDATING/POSTING data to the DB.
    if request.method == "POST":
        errors = Show.objects.validateShow(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f"/shows/{show_id}/updatePage")

    show = Show.objects.get(id=show_id)
    show.location = request.POST['location']
    show.start_date = request.POST['start_date']
    show.end_date = request.POST['end_date']
    show.description = request.POST['description']
    show.save()
    return redirect("/")


# **************************** Delete Page Logic *******************

def delete(request, show_id):
    delete_show = Show.objects.get(id=show_id)
    delete_show.delete()
    return redirect('/dashboard')
