from django.shortcuts import render, get_object_or_404, redirect
from .models import Manager
from posts.models import Posts
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def manager_list(request):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    manager = Manager.objects.all()

    return render(request, 'back/manager_list.html', {'manager':manager})


def manager_del(request, pk):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    manager = Manager.objects.get(pk=pk)
    b = User.objects.filter(username=manager.utxt)
    b.delete()

    manager.delete()

    return redirect('manager_list')


def manager_group(request):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    group = Group.objects.all().exclude(name="masteruser")

    return render(request, 'back/manager_group.html', {'group':group})


def manager_group_add(request):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check
    
    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    if request.method == 'POST':

        name = request.POST.get('name')

        if name != "":

            if len(Group.objects.filter(name=name)) == 0:

                group = Group(name=name)
                group.save()
            
            else:

                error = "This name already exists"
                return render(request, 'back/error.html', {'error':error})

    return redirect('manager_group')


def manager_group_del(request, name):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

     # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    b = Group.objects.filter(name=name)
    b.delete()

    return redirect('manager_group')


def users_groups(request, pk):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    manager = Manager.objects.get(pk=pk)

    user = User.objects.get(username=manager.utxt)

    ugroup = []

    for i in user.groups.all():
        ugroup.append(i.name)

    group = Group.objects.all()

    return render(request, 'back/users_groups.html', {'ugroup':ugroup, 'group':group, 'pk':pk})


def add_users_to_groups(request, pk):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    if request.method == 'POST':

        gname = request.POST.get('gname') # Name received from dropdown

        group = Group.objects.get(name=gname)
        manager = Manager.objects.get(pk=pk)
        user = User.objects.get(username=manager.utxt)
        user.groups.add(group)

    return redirect('users_groups', pk=pk)


def del_users_to_groups(request, pk, name):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    group = Group.objects.get(name=name)
    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.utxt)
    user.groups.remove(group)

    return redirect('users_groups', pk=pk)


def manager_perms(request):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    perms = Permission.objects.all()

    return render(request, 'back/manager_perms.html', {'perms':perms})

def manager_perms_del(request, name):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    perms = Permission.objects.filter(name=name)
    perms.delete()

    return redirect('manager_perms')

def manager_perms_add(request):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    if request.method == 'POST':

        name = request.POST.get('name')
        cname = request.POST.get('cname')
        
        if len(Permission.objects.filter(codename=cname)) == 0:

            content_type = ContentType.objects.get(app_label='main', model='main')
            permission = Permission.objects.create(codename=cname, name=name, content_type=content_type)

        else:
            error = "This codename already exists"
            return render(request, 'back/error.html', {'error':error})

    return redirect('manager_perms')


def users_perms(request, pk):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    manager = Manager.objects.get(pk=pk)

    user = User.objects.get(username=manager.utxt)

    permission = Permission.objects.filter(user=user)

    uperms = []
    for i in permission:
        uperms.append(i.name)

    perms = Permission.objects.all()    

    return render(request, 'back/users_perms.html', {'uperms':uperms, 'pk':pk, 'perms':perms})


def users_perms_del(request, pk, name):
# PK of user, name of perm    

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})    
    
    manager = Manager.objects.get(pk=pk)

    user = User.objects.get(username=manager.utxt)

    permission = Permission.objects.get(name=name)
    user.user_permissions.remove(permission)

    return redirect('users_perms', pk=pk)


def users_perms_add(request, pk):
    # PK of user, name of perm    

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})    

    if request.method == 'POST':

        pname = request.POST.get('pname')
    
        manager = Manager.objects.get(pk=pk)
        user = User.objects.get(username=manager.utxt)

        permission = Permission.objects.get(name=pname)
        user.user_permissions.add(permission)

    return redirect('users_perms', pk=pk)


def groups_perms(request, name):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    group = Group.objects.get(name=name)
    perms = group.permissions.all()

    allperms = Permission.objects.all()

    return render(request, 'back/groups_perms.html', {'perms':perms, 'name':name, 'allperms':allperms})


def groups_perms_del(request, gname, name):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    group = Group.objects.get(name=gname)
    perm = Permission.objects.get(name=name)

    group.permissions.remove(perm)

    return redirect('groups_perms', name=gname)


def groups_perms_add(request, name):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    # Lect 224
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    if request.method == 'POST':

        pname = request.POST.get('pname')

        group = Group.objects.get(name=name)
        perm = Permission.objects.get(name=pname)

        group.permissions.add(perm)

    return redirect('groups_perms', name=name)