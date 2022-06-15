from datetime import date
from django.forms import DateInput, DateTimeInput
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_login(request):
    error = ""
    if request.method=="POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"

            else:
                error = "yes"
        except:
            error = "yes"
    
    d = {'error':error}
    return render(request,'admin_login.html',d)

def user_login(request):
    error = ""
    if request.method == "POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u, password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == 'student':
                    login(request,user)
                    error  = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
        
    d = {'error':error}
    return render(request,'user_login.html',d)

def user_signup(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        c = request.POST['contact']
        g = request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f, username=e, password=p, last_name=l)
            StudentUser.objects.create(user=user, mobile=c,image=i,gender=g,type="student")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request,'user_signup.html')

def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == 'recruiter' and user1.status!="pending":
                    login(request,user)
                    error  = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
        
    d = {'error':error}
    return render(request,'recruiter_login.html',d)

def recruiter_signup(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        c = request.POST['contact']
        g = request.POST['gender']
        co = request.POST['company']
        try:
            user = User.objects.create_user(first_name=f, username=e, password=p, last_name=l)
            Recruiter.objects.create(user=user, mobile=c,image=i,gender=g,company=co,type="recruiter",status="pending")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request,'recruiter_signup.html',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user= request.user
    student = StudentUser.objects.get(user = user)
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        g = request.POST['gender']

        student.user.first_name = f
        student.user.last_name = l
        student.mobile = c
        student.recruiter = g
        try:
            student.save()
            student.user.save()
            error = "no"
        except:
            error = "yes"

            try:
                i = request.FILES['image']
                student.image = i
                student.save()
                error = "no"
            except:
                pass

    d = {'student':student,'error':error}
    return render(request,'user_home.html',d)

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user= request.user
    recruiter = Recruiter.objects.get(user = user)
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        g = request.POST['gender']

        recruiter.user.first_name = f
        recruiter.user.last_name = l
        recruiter.mobile = c
        recruiter.recruiter = g
        try:
            recruiter.save()
            recruiter.user.save()
            error = "no"
        except:
            error = "yes"

            try:
                i = request.FILES['image']
                recruiter.image = i
                recruiter.save()
                error = "no"
            except:
                pass

    d = {'recruiter':recruiter,'error':error}
    return render(request,'recruiter_home.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount = Recruiter.objects.all().count()
    scount = StudentUser.objects.all().count()
    d = {'rcount':rcount, 'scount':scount}
    return render(request,'admin_home.html',d)

def view_user(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    d = {'data': data}
    return render(request, 'view_user.html',d)


def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='pending')
    d = {'data': data}
    return render(request, 'recruiter_pending.html',d)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Accept')
    d = {'data': data}
    return render(request, 'recruiter_accepted.html',d)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.all()
    d = {'data': data}
    return render(request, 'recruiter_all.html',d)

def delete_recruiter(request,pid):
    recruiter = User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')


def delete_user(request,pid):
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_user')


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                 error = "not"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'change_passwordadmin.html',d)


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                 error = "not"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'change_passworduser.html',d)


def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                 error = "not"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'change_passwordrecruiter.html',d)


def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method=='POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        l = request.FILES['logo']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,startdate=sd,enddate=ed,title=jt,salary=sal,image=l,description=des,experience=exp,location=loc,skills=skills)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request,'add_job.html')

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    d = {'job': job}
    return render(request,'job_list.html',d)


def latest_jobs(request):
    job = Job.objects.all().order_by('-startdate')
    d = {'job': job}
    return render(request, 'latest_jobs.html',d)

def user_latestjobs(request):
    job = Job.objects.all().order_by('-startdate')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = apply.objects.filter(student=student)
    li = []
    for i in data:
        li.append(i.job.id)
    d = {'job': job,'li':li}
    return render(request, 'user_latestjobs.html',d)


def job_detail(request,pid):
    job = Job.objects.get(id=pid)
    d = {'job': job}
    return render(request, 'job_detail.html',d)


def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    user=request.user
    student = StudentUser.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1 = date.today()
    if job.enddate < date1:
        error = "close"
    elif job.startdate > date1:
        error =  "notopen"
    else: 
        if request.method == 'POST':
            r = request.FILES['resume']
            apply.objects.create(job=job,student=student,resume=r,applydate=date.today())
            error = "done"

    d = {'error':error}
    return render(request,'applyforjob.html',d)


def applied_candidate(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    data = apply.objects.all()
    d = {'data':data}
    return render(request,'applied_candidate.html',d)

def contact(request):
    return render(request,'contact.html')

def Logout(request):
    logout(request)
    return redirect('index')
