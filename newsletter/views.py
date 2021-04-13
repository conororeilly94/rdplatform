from django.shortcuts import render, get_object_or_404, redirect
from .models import Newsletter
from posts.models import Posts
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def news_letter(request):

    if request.method == 'POST':

        txt = request.POST.get('txt')

        res = txt.find('@')
        
        if int(res) != -1:
            b = Newsletter(txt=txt, status=1)
            b.save()
        else:
            try:
                int(txt)
                b = Newsletter(txt=txt, status=2)
                b.save()
            except:
                return redirect('home')

    return redirect('home')


def news_emails(request):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    emails = Newsletter.objects.filter(status=1)

    return render(request, 'back/emails.html', {'emails':emails})


def news_phones(request):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    phones = Newsletter.objects.filter(status=2)

    return render(request, 'back/phones.html', {'phones':phones})


def news_txt_del(request, pk, num):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    b = Newsletter.objects.get(pk=pk)
    b.delete()

    if int(num) == 2:
        return redirect('news_phones')

    return redirect('news_emails')