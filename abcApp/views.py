from asyncio.windows_events import NULL
from logging import error
from pickle import NONE
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from abcApp.forms import *
from .models import *
import datetime

# Create your views here.
def home(request):
    context = {}
    return render(request, 'pages/home.html', context)

def admin_create(request):
    user = request.user
    
    if not user.is_authenticated:
        return redirect('login')

    if user.role != "admin": 
        return HttpResponse("You are not an Admin")
    
    context = {}
    if request.POST:
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            context['msg'] = request.POST['user_id'] + " is created."

        else:
            context['signup_form'] = form

    else:
        form = AdminSignUpForm()
        context['signup_form'] = form
    
    return render(request, 'admin/createAccount.html', context)

def user_login(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('homepage')
    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            user_id = request.POST['user_id']
            password = request.POST['password']
            user = authenticate(username=user_id,password=password)
            if user is not None:
                login(request, user)
                if user.role == "child":
                    return redirect('upload')
                return redirect('homepage')
    else:
        form = UserAuthenticationForm()
    
    context['login_form'] = form
    return render(request, 'user/login.html', context)

def user_logout(request):
    logout(request)
    return render(request, 'user/logout.html')

def user_register(request):
    user = request.user
    if user.is_authenticated: 
        return HttpResponse("You are already logged in as " + str(user.user_id))
    
    context = {}
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user_id = form.cleaned_data.get('user_id')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user_id, password=password)
            login(request, user)            
            return redirect('homepage')
        else:
            print(form.errors["password2"])
            context['signup_form'] = form

    else:
        form = SignUpForm()
        context['signup_form'] = form
    
    return render(request, 'user/signup.html', context)

def user_edit(request):
    user = request.user
    if not user.is_authenticated: 
        return redirect ('login')
    context = {}

    if request.POST:
        form = UserUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            user.set_password(request.POST['newPass'])
            return redirect('editAcc')

    else:
        initialData = {"user_id": user.user_id}
        form = UserUpdateForm(initial=initialData)
        context['user_update_form'] = form

    return render(request, 'user/editAcc.html', context)

def request(request):
    context = {}
    user = request.user
    allRequest = Request.objects.filter(isCompleted = False)
    context['allRequest'] = allRequest

    if user.is_anonymous:
        user.role = "Anon"
        
    if user.role == "Anon" or user.role=="user":
        return render(request, 'pages/request.html', context)
    
    elif user.role == "admin":
        if request.POST:
            form = RequestCreationForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                context['request_form'] = form
        else:
            form = RequestCreationForm()
            context['request_form'] = form

        return render(request, 'admin/request.html', context)

def removeRequest(request):
    requestItem = request.POST.get('item','')
    print("removing request")
    print(requestItem)
    try:
        obj = Request.objects.get(id = requestItem)
        obj.isCompleted = True
        obj.isPerm = False
        obj.save()
    except:
        print("Not Found")

    return redirect('request')

def requestCompleted(request):
    requestItem = request.GET.get('item','')
    item = None
    object = None
    try:
        obj = Request.objects.get(id = requestItem)
        if not obj.isPerm:
            obj.isCompleted = True
            obj.save()
        item = obj.request_Obj
        object = obj
    except:
        item = "Not Found"

    context = {}
    userID = None
    if request.user.is_anonymous:
        userID = "Anonymous"
    else:
        userID = request.user.user_id

    context['user'] = userID
    context['item'] = item
    context['object'] = object

    if request.POST:
        form = RequestDonationForm(request.POST)
        if form.is_valid():
            form.instance.request = object
            form.save()
            return redirect('request')
        else:
            context['donate_form'] = form
    else:
        form = RequestDonationForm()
        context['donate_form'] = form

    return render(request, 'pages/requestCompleted.html', context)

def visit(request):
    context = {}
    user = request.user
    
    if not user.is_authenticated:
        return redirect('login')
        
    if user.role=="user":
        allAcceptedVisits = Visit.objects.filter(user=user, visit_date__gte=datetime.date.today(), status="Accepted")
        allUserVisits = Visit.objects.filter(user=user, visit_date__gte=datetime.date.today(), responded=False)
        print(allAcceptedVisits)
        context['acceptedVisits'] = allAcceptedVisits
        context['visits'] = allUserVisits

        if request.POST:
            form = VisitCreationForm(request.POST)
            if form.is_valid():
                form.instance.user = user
                form.save()
            else:
                context['visit_form'] = form
        else:
            form = VisitCreationForm()
            context['visit_form'] = form
        return render(request, 'pages/visit.html', context)
    
    elif user.role == "admin":
        allAcceptedVisits = Visit.objects.filter(visit_date__gte=datetime.date.today(), status="Accepted")
        allVisits = Visit.objects.filter(responded=False)
        context['visits'] = allVisits
        context['acceptedVisits'] = allAcceptedVisits
        return render(request, 'admin/visit.html', context)

    return render(request, 'pages/visit.html', context)

def AcceptOrRejectVisit(request):
    accept = request.POST.get('accept','')
    reject = request.POST.get('reject','')

    if accept != "":
        try:
            obj = Visit.objects.get(id = accept)
            obj.responded = True
            obj.status = "Accepted"
            obj.save()
        except:
            print("Not Found")
    elif reject != "":
        try:
            obj = Visit.objects.get(id = reject)
            obj.responded = True
            obj.status = "Rejected"
            obj.save()
        except:
            print("Not Found")

    return redirect('visit')

def donate(request):
    context = {}
    user = request.user
    context['user'] = user

    if user.is_authenticated:
        try:
            allYearlyDonation = MoneyDonation.objects.filter(donatedBy=user.user_id, yearly=True)
            context['yearlyDonation'] = allYearlyDonation
            
        except:
            DO_NOTHING

    if request.POST:
        form = DonationCreationForm(request.POST)
        if form.is_valid():
            if user.is_authenticated:
                form.instance.donatedBy = user
            if request.POST['txtIC']:
                form.instance.nric = request.POST['txtIC']
            qty = 0 
            if request.POST['donation'] == 'others':
                qty = request.POST['inputDonation']
            else:
                qty = request.POST['donation']
            form.instance.qty = qty
            form.instance.date = datetime.date.today()
            context['msg'] = "Thank You for donating to us $" + qty + "."
            form.save()
        else:
            context['money_form'] = form
    else:
        form = DonationCreationForm()
        context['money_form'] = form
    return render(request, 'pages/donate.html', context)

def works(request):
    context = {}
    user = request.user
    allWorks = Upload.objects.all().order_by('likes')
    worksType = []
    for i in allWorks:
        worksType.append(i.child_object.name.split('.')[-1])
    context['works'] = allWorks
    context['worksType'] = worksType
    context['user'] = user
    return render(request, 'pages/works.html', context)

def uploadWork(request):
    context = {}
    user = request.user
    if not user.is_authenticated: 
        return redirect ('login')

    if not user.role == "child":
        return redirect('login')

    if request.POST:
        form = WorkCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.child_id = user
            form.save()
            context['msg'] = request.FILES['child_object'].name + " have been uploaded."
        else:
            context['upload_form'] = form
    else:
        form = WorkCreationForm()
        context['upload_form'] = form

    return render(request, 'child/submission.html', context)

def like(request, upload_id):
    context = {}
    try: 
        obj = Upload.objects.get(id=upload_id)
        obj.likes +=1
        obj.save()
    except:
        print("ID NOT Found")

    return redirect('childrenWork')

def cancel(request, md_id):
    context = {}
    print("cancel")
    print(MoneyDonation.objects.get(id=md_id))
    try: 
        obj = MoneyDonation.objects.get(id=md_id)
        obj.yearly = False
        obj.save()
    except:
        print("ID NOT Found")

    return redirect('donate')


def contact(request):
    context = {}
    return render(request, 'pages/contact.html', context)