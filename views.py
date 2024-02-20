from django.shortcuts import render, redirect
from .models import Account, Status 
from .form import UserAccountForm 
from django.contrib.auth import logout

def signup(request):
    return render(request, 'signup.html')

def signupaction(request):
    if request.method == 'POST':
        username = request.POST['txtusername']
        password = request.POST['txtpassword']
        firstname = request.POST['txtfirstname']
        lastname = request.POST['txtlastname']
        address = request.POST['txtaddress']
        mobile = request.POST['txtmobile']
        email2 = request.POST['txtemail']
        status = 0
        role = 'user'
        account = Account.objects.create(username=username, password=password, role=role,
                                                  firstname=firstname, lastname=lastname, address=address,
                                                  mobile=mobile, email=email2, status=status)
        try:
            account.save()
            return redirect(login)
        except:
            errmsg = 'User Registration Failed'
            return render(request, 'signup.html', {'errmsg': errmsg})
    else:
        return redirect(signup)


def home(request):
    role = request.session['role']
    if role == 'admin':
        return render(request, 'adminhome.html')
    else:
        return render(request, 'userhome.html')


def login(request):
    form = UserAccountForm()
    return render(request, 'login.html', {'form': form})


def loginaction(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = Account.objects.filter(username=username, password=password, status=1).first()
        if user:
            Status.objects.update_or_create(username=username, defaults={'status': 'Online'})
            request.session['username'] = user.username
            request.session['role'] = user.role
            if user.role == "admin":
                return render(request, 'adminhome.html')
            else:
                return render(request, 'userhome.html')
        else:
            form = UserAccountForm()
            return render(request, 'login.html', {'errmsg': 'Invalid username or password, or your account is not approved by the admin', 'form': form})
    else:
        return redirect(login)


def logout(request):
    Status.objects.update_or_create(username=request.session.get('username'), defaults={'status': 'Offline'})
    request.session.flush()
    return redirect('login')

def editlogin(request, username):
    login = Account.objects.get(username=username)
    return render(request, 'editlogin.html', {'login': login})


def updatelogin(request, id):
    login = Account.objects.get(userid=id)
    if request.method == 'POST':
        pass 
    else:
        return render(request, 'editlogin.html', {'login': login})


def deletelogin(request, id):
    login = Account.objects.get(userid=id)
    login.delete()
    logins = Account.objects.all()
    return render(request, 'adminhome.html', {'logins': logins})


def editprofile(request):
    username = request.session['username']
    login = Account.objects.get(username=username)
    return render(request, 'editprofile.html', {'login': login})


def updateprofile(request):
    username=request.session['username']
    firstname=request.POST['txtfirstname']
    lastname=request.POST['txtlastname']
    address=request.POST['txtaddress']
    mobile=request.POST['txtmobile']
    email=request.POST['txtemail']
    login=Account.objects.get(username=username)
    try:
        login.firstname=firstname
        login.lastname=lastname
        login.address=address
        login.mobile=mobile
        login.email=email
        login.save()
        return redirect(home)
    except:
        errmsg='Update Failed'
        username=request.session['username']
        login = Account.objects.get(username=username)
        return render(request,'editprofile.html', {'login':login,'errmsg':errmsg})


def custom_logout(request):
    logout(request)
    return redirect('login')

def changepassword(request):
    return render(request, 'changepassword.html')


def updatepassword(request):
    password=request.POST['password']
    newpassword=request.POST['newpassword']
    confirmpassword=request.POST['confirmpassword']
    username=request.session['username']
    login=Account.objects.get(username=username)
    p=login.password
    if p==password:
        if newpassword==confirmpassword:
            login.password=newpassword
            login.save()
            errmsg='Password changed successfully'
            return render(request,'changepassword.html',{'errmsg':errmsg})
        else:
            errmsg='New Password and Confirm Password must be the same'
            return render(request,'changepassword.html',{'errmsg':errmsg})
    else:
        errmsg='Invalid Current Password'
        return render(request,'changepassword.html',{'errmsg':errmsg})


def validateuser(request):
    logins = Account.objects.filter(status=0)
    return render(request, 'validateuser.html', {'logins': logins})

def approveuser(request, username):
    login = Account.objects.get(username=username)
    login.status = 1
    login.save()
    return redirect(validateuser)



def rejectuser(request, username):
    login = Account.objects.get(username=username)
    login.delete()
    return redirect(validateuser)


def editusers(request):
    logins = Account.objects.all()
    return render(request, 'editusers.html', {'logins': logins})


def profilebase(request):
    user_accounts = Account.objects.order_by('username')
    status_list = Status.objects.order_by('username')
    return render(request, "profilebase.html", {'user_accounts': user_accounts, 'status_list': status_list})
