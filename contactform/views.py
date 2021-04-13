from django.shortcuts import render, get_object_or_404, redirect
from .models import ContactForm
from posts.models import Posts
from category.models import Category
from subcategory.models import SubCategory
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
import datetime

# Create your views here.

def contact_add(request):

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)

    today = str(year) + "/" + str(month) + "/" + str(day)
    time = str(now.hour) + ":" + str(now.minute)

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')

        if name == "" or email == "" or text == "":
            
            msg = "All Fields Required"
            return render(request, 'front/message.html', {'msg':msg})

        b = ContactForm(name = name, email = email, text = text, date = today, time = time)
        b.save()
        msg = "Your Message has Been Recieved"
        return render(request, 'front/message.html', {'msg':msg})

    return render(request, 'front/message.html')


def contact_show(request):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    msg = ContactForm.objects.all()

    return render(request, 'back/contact_form.html', {'msg':msg})


def contact_del(request, pk):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    b = ContactForm.objects.filter(pk = pk)
    b.delete()

    return redirect('contact_show')