from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from users.models import UserRegistration

def AdminHome(request):
    return render(request, 'admins/admihomepage.html')

def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pswd']
        print("Admin:", username, password)
        if username == 'admin' and password == 'admin':
            return redirect('adminhome')
        return redirect('userLogin')
    return render(request, 'adminLogin.html')

def ActivatedUsers(request):
    users = UserRegistration.objects.all()
    return render(request, 'admins/activatedlist.html', {'users': users})

def UserActivate(request, pk):
    user = get_object_or_404(UserRegistration, id=pk)
    if not user.is_active:
        user.is_active = True
        user.save()
        return redirect(ActivatedUsers)
    # return render(request, 'admins/activatedlist.html')

def BlockUser(request, pk1):
    user = get_object_or_404(UserRegistration, id=pk1)
    if user.is_active:
        user.is_active = False
        user.save()
    return redirect(ActivatedUsers)

def AdminLogout(request):
    logout(request)
    return redirect('adminLogin')
