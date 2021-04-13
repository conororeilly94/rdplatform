# ACTIONS
from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from posts.models import Posts
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group, Permission
from manager.models import Manager
import random
import string
from random import randint

# Create your views here.

def home(request):

    site = Main.objects.get(pk=2)
    posts = Posts.objects.filter(act=1).order_by('-pk')
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    lastposts = Posts.objects.filter(act=1).order_by('-pk')[:3]
    popularposts = Posts.objects.filter(act=1).order_by('-views')
    popularposts2 = Posts.objects.filter(act=1).order_by('-views')[:3]
    lastposts2 = Posts.objects.filter(act=1).order_by('-pk')[:4]

    return render(request, 'front/home.html', {'site':site, 'posts':posts, 'category':category, 'subcategory':subcategory, 'lastposts':lastposts, 'popularposts':popularposts, 'popularposts2':popularposts2, 'lastposts2':lastposts2})
    
def about(request):

    site = Main.objects.get(pk=2)
    posts = Posts.objects.all().order_by('-pk')
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    lastposts = Posts.objects.all().order_by('-pk')[:3]
    popularposts2 = Posts.objects.all().order_by('-views')[:3]

    return render(request, 'front/about.html', {'site':site, 'posts':posts, 'category':category, 'subcategory':subcategory, 'lastposts':lastposts, 'popularposts2':popularposts2})


def panel(request):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    perm = 0
    perms = Permission.objects.filter(user=request.user)
    for i in perms:
        if i.codename == "master_user" : perm = 1

    # test = ['!', '@', '#', '$', '%']
    # rand = ""
    # for i in range(5):
    #     rand = rand + random.choice(string.ascii_letters)
    #     rand += random.choice(test)
    #     rand += str(random.randint(0,9))

    # count = Posts.objects.count()
    # rand = Posts.objects.all()[randint(0,count-1)]

    return render(request, 'back/home.html', {})


def mylogin(request):

    if request.method == 'POST':

        # 182
        uuser = request.POST.get('username')
        upassword = request.POST.get('password')

        if uuser != "" and upassword != "":

            user = authenticate(username = uuser, password = upassword)

            if user != None:

                login(request, user)
                return redirect('panel')

    return render(request, 'front/login.html')


def myregister(request):
    
    if request.method == 'POST':

        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if name == "":
            msg = "Please Input your Name"
            return render(request, 'front/message.html', {'msg': msg})

        # Check if passwords match
        if pass1 != pass2:
            msg = "Your Passwords do not Match"
            return render(request, 'front/message.html', {'msg': msg})

        # Check strenth of new password
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0

        for i in pass1 :

            if i > "0" and i < "9" :
                count1 = 1
            if i > "A" and i < "Z" :
                count2 = 1
            if i > 'a' and i < 'z' :
                count3 = 1
            if i > "!" and i < "@" :
                count4 = 1

        if count1 == 0 or count2 == 0 or count3 == 0 or count4 == 0:
            msg = "Your Passwords is Not Strong Enough"
            return render(request, 'front/message.html', {'msg': msg})

        # Contains at least 8 chars
        if len(pass1) < 8:
            msg = "Your Passwords must be at Least 8 Characters"
            return render(request, 'front/message.html', {'msg': msg})

        # If user and email not in DB, then create user
        if len(User.objects.filter(username = uname)) == 0 and len(User.objects.filter(email = email)) == 0:
            user = User.objects.create_user(username = uname, email = email, password = pass1)
            b = Manager(name = name, utxt = uname, email = email)
            b.save()

    return render(request, 'front/login.html')


def mylogout(request):

    logout(request)

    return redirect('mylogin')


def site_setting(request):

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
        about = request.POST.get('about')
        sname = request.POST.get('set_name')

        if name == "" or about == "" or sname == "":

            error = "All Fields Required"
            return render(request, 'back/error.html', {'error':error})

        try: 

            myfile = request.FILES['myfile']
            fs = FileSystemStorage() # Make an object
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            logourl = url
            logoname = filename

        except:

            logourl = "-"
            logoname = "-"

        try: 

            myfile2 = request.FILES['myfile2']
            fs2 = FileSystemStorage() # Make an object
            filename2 = fs2.save(myfile2.name, myfile2)
            url2 = fs2.url(filename2)

            logourl2 = url2
            logoname2 = filename2

        except:

            logourl2 = "-"
            logoname2 = "-"

        b = Main.objects.get(pk=2)
        b.name = name
        b.about = about
        b.sname = sname

        if logourl != "-" : b.logourl = logourl
        if logoname != "-" : b.logoname = logoname
        if logourl2 != "-" : b.logourl2 = logourl2
        if logoname2 != "-" : b.logoname2 = logoname2

        b.save()        

    site = Main.objects.get(pk=2)

    return render(request, 'back/setting.html', {'site':site})


def about_setting(request):

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

    if request.method == "POST":

        text = request.POST.get('text')

        if text == "":

            error = "All Fields Required"
            return render(request, 'back/error.html', {'error':error})

        b = Main.objects.get(pk=2)
        b.abouttext = text
        b.save()

    about = Main.objects.get(pk=2).abouttext

    return render(request, 'back/about_setting.html', {'about':about})


def contact(request):

    site = Main.objects.get(pk=2)
    posts = Posts.objects.all().order_by('-pk')
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    lastposts = Posts.objects.all().order_by('-pk')[:3]
    popularposts2 = Posts.objects.all().order_by('-views')[:3]

    return render(request, 'front/contact.html', {'site':site, 'posts':posts, 'category':category, 'subcategory':subcategory, 'lastposts':lastposts, 'popularposts2':popularposts2})


def change_pass(request):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    if request.method == 'POST':

        # Get input
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == "" or newpass == "":

            error = "All Fields Required"
            return render(request, 'back/error.html', {'error':error})

        user = authenticate(username = request.user, password = oldpass)

        if user != None:

            if len(newpass) < 8:

                error = "Your Password Must be at least 8 Characters"
                return render(request, 'back/error.html', {'error':error})

            # Check strenth of new password
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0

            for i in newpass :
    
                if i > "0" and i < "9" :
                    count1 = 1
                if i > "A" and i < "Z" :
                    count2 = 1
                if i > 'a' and i < 'z' :
                    count3 = 1
                if i > "!" and i < "@" :
                    count4 = 1

            if count1 == 1 and count2 == 1 and count3 == 1 and count4 == 1 :

                user = User.objects.get(username=request.user)
                user.set_password(newpass)
                user.save()
                return redirect('mylogout')

            print(count1, count2, count3, count4)

        else:

            error = "Your Password is Incorrect"
            return render(request, 'back/error.html', {'error':error})


    return render(request, 'back/changepass.html')


def answer_contactform(request, pk):


    return render(request, 'back/answer_contactform.html', {'pk':pk})
