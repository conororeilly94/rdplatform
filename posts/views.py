from django.shortcuts import render, get_object_or_404, redirect
from .models import Posts
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcategory.models import SubCategory
from category.models import Category
import random
from comment.models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain

# Create your views here.

def posts_detail(request, word):
    
    site = Main.objects.get(pk=2)
    posts = Posts.objects.all().order_by('-pk')
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    lastposts = Posts.objects.all().order_by('-pk')[:3]

    showposts = Posts.objects.filter(name=word)
    popularposts = Posts.objects.all().order_by('-views')
    popularposts2 = Posts.objects.all().order_by('-views')[:3]

    tagname = Posts.objects.get(name=word).tag
    tag = tagname.split(',')

    try:
        # View count
        myposts = Posts.objects.get(name=word)
        myposts.views = myposts.views + 1
        myposts.save()
    
    except:

        print("Can't Add Show")

    code = Posts.objects.get(name=word).pk
    comment = Comment.objects.filter(posts_id=code, status=1).order_by('-pk')[:3]
    cmcount = len(comment)

    return render(request, 'front/posts_detail.html', {'posts':posts, 'site':site, 'posts':posts, 'category':category, 
                            'subcategory':subcategory, 'lastposts':lastposts, 'showposts':showposts, 'popularposts':popularposts, 
                            'popularposts2':popularposts2, 'tag':tag, 'code':code, 'comment':comment, 'cmcount':cmcount})


def posts_detail_short(request, pk):
    
    site = Main.objects.get(pk=2)
    posts = Posts.objects.all().order_by('-pk')
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    lastposts = Posts.objects.all().order_by('-pk')[:3]

    showposts = Posts.objects.filter(rand=pk)
    popularposts = Posts.objects.all().order_by('-views')
    popularposts2 = Posts.objects.all().order_by('-views')[:3]

    tagname = Posts.objects.get(rand=pk).tag
    tag = tagname.split(',')

    try:
        # View count
        myposts = Posts.objects.get(rand=pk)
        myposts.views = myposts.views + 1
        myposts.save()
    
    except:

        print("Can't Add Show")

    return render(request, 'front/posts_detail.html', {'posts':posts, 'site':site, 'posts':posts, 'category':category, 'subcategory':subcategory, 'lastposts':lastposts, 'showposts':showposts, 'popularposts':popularposts, 'popularposts2':popularposts2, 'tag':tag})


def posts_list(request):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        posts = Posts.objects.filter(author=request.user)
    elif perm == 1:
        postss = Posts.objects.all()
        paginator = Paginator(postss,5)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)

        except EmptyPage:
            posts = paginator.page(paginator.num_page)

        except PageNotAnInteger:
            posts = paginator.page(1)

    
    return render(request, 'back/posts_list.html', {'posts':posts})


def posts_add(request):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

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

    date = str(year) + str(month) + str(day)
    randint = str(random.randint(1000,9999))
    rand = date + randint
    rand = int(rand)

    while len(Posts.objects.filter(rand=rand)) != 0:
        randint = str(random.randint(1000,9999))
        rand = date + randint
        rand = int(rand)

    category = SubCategory.objects.all()    

    if request.method == 'POST':

        poststitle = request.POST.get('poststitle')
        postscat = request.POST.get('postscat')
        postsummary = request.POST.get('postsummary')
        postbody = request.POST.get('postbody')
        postid = request.POST.get('postscat')
        tag = request.POST.get('tag')

        if poststitle == '' or postsummary == '' or postbody == '' or postscat == '':
            error = "All Fields are Required"
            return render(request, 'back/error.html', {'error':error})

        try:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage() # Make an object
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000:

                    postname = SubCategory.objects.get(pk=postid).name
                    ocatid = SubCategory.objects.get(pk=postid).catid

                    b = Posts(name = poststitle, short_txt = postsummary, body_txt = postbody, date = today, img = filename, imgurl = url, 
                                author = request.user, catname = postname, catid = postid, views = 0, time = time, ocatid = ocatid, tag = tag, rand=rand)
                    b.save()

                    count = len(Posts.objects.filter(ocatid = ocatid))

                    b = Category.objects.get(pk = ocatid)
                    b.count = count
                    b.save()

                    return redirect('posts_list')

                else:

                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your File is Larger than 5 MB"
                    return render(request, 'back/error.html', {'error':error})
            
            else:

                fs = FileSystemStorage()
                fs.delete(filename)

                # Come back to lecture 148
                error = "Your File is Not Supported"
                return render(request, 'back/error.html', {'error':error})

        except:

            error = "Please Input Your Content"
            return render(request, 'back/error.html', {'error':error})
    
    return render(request, 'back/posts_add.html', {'category':category})


def posts_delete(request, pk):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        a = Posts.objects.get(pk=pk).author
        if str(a) != str(request.user):
            error = "Access Denied"
            return render(request, 'back/error.html', {'error':error})

    try:

        b = Posts.objects.get(pk=pk)

        fs = FileSystemStorage()
        fs.delete(b.img)

        ocatid = Posts.objects.get(pk=pk).ocatid

        b.delete()
        
        count = len(Posts.objects.filter(ocatid = ocatid))

        m = Category.objects.get(pk = ocatid)
        m.count = count
        m.save()

    except:

        error = "Something Went Wrong"
        return render(request, 'back/error.html', {'error':error})

    return redirect('posts_list')


def posts_edit(request, pk):

    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    if len(Posts.objects.filter(pk=pk)) == 0:
        error = "Post Does Not Exist"
        return render(request, 'back/error.html', {'error':error})

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0:
        a = Posts.objects.get(pk=pk).author
        if str(a) != str(request.user):
            error = "Access Denied"
            return render(request, 'back/error.html', {'error':error})

    posts = Posts.objects.get(pk=pk)
    category = SubCategory.objects.all()

    if request.method == 'POST':
    
        poststitle = request.POST.get('poststitle')
        postscat = request.POST.get('postscat')
        postsummary = request.POST.get('postsummary')
        postbody = request.POST.get('postbody')
        postid = request.POST.get('postscat')
        tag = request.POST.get('tag')

        if poststitle == '' or postsummary == '' or postbody == '' or postscat == '':
            error = "All Fields are Required"
            return render(request, 'back/error.html', {'error':error})

        try: 

            myfile = request.FILES['myfile']
            fs = FileSystemStorage() # Make an object
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000:

                    postname = SubCategory.objects.get(pk=postid).name

                    b = Posts.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(b.img)

                    b.name = poststitle
                    b.short_txt = postsummary
                    b.body_txt = postbody
                    b.img = filename
                    b.imgurl = url
                    b.catname = postname
                    b.catid = postid
                    b.tag = tag
                    b.act = 0

                    b.save()
                    return redirect('posts_list')

                else:

                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your File is Larger than 5 MB"
                    return render(request, 'back/error.html', {'error':error})
            
            else:

                fs = FileSystemStorage()
                fs.delete(filename)

                # Come back to lecture 148
                error = "Your File is Not Supported"
                return render(request, 'back/error.html', {'error':error})

        except:

            postname = SubCategory.objects.get(pk=postid).name

            b = Posts.objects.get(pk=pk)

            b.name = poststitle
            b.short_txt = postsummary
            b.body_txt = postbody
            b.catname = postname
            b.catid = postid
            b.tag = tag

            b.save()
            return redirect('posts_list')
    
    return render(request, 'back/posts_edit.html', {'pk':pk, 'posts':posts, 'category':category})


def posts_publish(request, pk):
    
    # Authenticating user
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # End login check

    posts = Posts.objects.get(pk=pk)
    posts.act = 1
    posts.save()

    return redirect('posts_list')


def posts_all_show(request, word):

    catid = Category.objects.get(name=word).pk
    allposts = Posts.objects.filter(ocatid=catid)

    site = Main.objects.get(pk=2)
    posts = Posts.objects.filter(act=1).order_by('-pk')
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    lastposts = Posts.objects.filter(act=1).order_by('-pk')[:3]
    popularposts = Posts.objects.filter(act=1).order_by('-views')
    popularposts2 = Posts.objects.filter(act=1).order_by('-views')[:3]
    lastposts2 = Posts.objects.filter(act=1).order_by('-pk')[:4]

    return render(request, 'front/all_posts.html', {'site':site, 'posts':posts, 'category':category, 'subcategory':subcategory, 'lastposts':lastposts, 'popularposts':popularposts, 'popularposts2':popularposts2, 'lastposts2':lastposts2, 'allposts':allposts})
    

def all_posts(request):
    
    allposts = Posts.objects.all()

    site = Main.objects.get(pk=2)
    posts = Posts.objects.filter(act=1).order_by('-pk')
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    lastposts = Posts.objects.filter(act=1).order_by('-pk')[:3]
    popularposts = Posts.objects.filter(act=1).order_by('-views')
    popularposts2 = Posts.objects.filter(act=1).order_by('-views')[:3]
    lastposts2 = Posts.objects.filter(act=1).order_by('-pk')[:4]

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)

    today = str(year) + "/" + str(month) + "/" + str(day)

    f_rom = []
    t_o = []

    for i in range(30):

        b = datetime.datetime.now() - datetime.timedelta(days=i)

        year = b.year
        month = b.month
        day = b.day

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)
        
        b = str(year) + "/" + str(month) + "/" + str(day)

        f_rom.append(b)

    for i in range(30):
    
        b = datetime.datetime.now() - datetime.timedelta(days=i)

        year = b.year
        month = b.month
        day = b.day

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)
        
        b = str(year) + "/" + str(month) + "/" + str(day)

        t_o.append(b)

    return render(request, 'front/all_posts_full.html', {'site':site, 'posts':posts, 'category':category, 'subcategory':subcategory, 'lastposts':lastposts, 'popularposts':popularposts, 'popularposts2':popularposts2, 'lastposts2':lastposts2, 'allposts':allposts, 'f_rom':f_rom, 't_o':t_o})


def all_posts_search(request):

    if request.method == 'POST':

        txt = request.POST.get('txt')
        catid = request.POST.get('category')
        f_rom = request.POST.get('from')
        t_o = request.POST.get('to')
        
        if f_rom != "0" and t_o != "0":

            if t_o < f_rom:

                msg = "To Date must not be less than From Date"
                return render(request, 'front/message.html', {'msg': msg})

    if catid == "0":

        if f_rom != "0" and t_o != "0":
            a = Posts.objects.filter(name__contains=txt,date__gte=f_rom, date__lte=t_o)
            b = Posts.objects.filter(short_txt__contains=txt, date__gte=f_rom, date__lte=t_o)
            c = Posts.objects.filter(body_txt__contains=txt, date__gte=f_rom, date__lte=t_o)

        elif f_rom != "0":
            a = Posts.objects.filter(name__contains=txt,date__gte=f_rom)
            b = Posts.objects.filter(short_txt__contains=txt, date__gte=f_rom)
            c = Posts.objects.filter(body_txt__contains=txt, date__gte=f_rom)

        elif t_o != "0":
            a = Posts.objects.filter(name__contains=txt, date__lte=t_o)
            b = Posts.objects.filter(short_txt__contains=txt, date__lte=t_o)
            c = Posts.objects.filter(body_txt__contains=txt, date__lte=t_o)

        else:
            a = Posts.objects.filter(name__contains=txt)
            b = Posts.objects.filter(short_txt__contains=txt)
            c = Posts.objects.filter(body_txt__contains=txt)

    else:

        if f_rom != "0" and t_o != "0":
            a = Posts.objects.filter(name__contains=txt, ocatid=catid, date__gte=f_rom, date__lte=t_o)
            b = Posts.objects.filter(short_txt__contains=txt, ocatid=catid, date__gte=f_rom, date__lte=t_o)
            c = Posts.objects.filter(body_txt__contains=txt, ocatid=catid, date__gte=f_rom, date__lte=t_o)

        elif f_rom != "0":
            a = Posts.objects.filter(name__contains=txt, ocatid=catid, date__gte=f_rom)
            b = Posts.objects.filter(short_txt__contains=txt, ocatid=catid, date__gte=f_rom)
            c = Posts.objects.filter(body_txt__contains=txt, ocatid=catid, date__gte=f_rom)

        elif t_o != "0":
            a = Posts.objects.filter(name__contains=txt, ocatid=catid, date__lte=t_o)
            b = Posts.objects.filter(short_txt__contains=txt, ocatid=catid, date__lte=t_o)
            c = Posts.objects.filter(body_txt__contains=txt, ocatid=catid, date__lte=t_o)

        else:
            a = Posts.objects.filter(name__contains=txt, ocatid=catid)
            b = Posts.objects.filter(short_txt__contains=txt, ocatid=catid)
            c = Posts.objects.filter(body_txt__contains=txt, ocatid=catid)

    # Merge queries
    allposts = list(chain(a,b,c))
    allposts = list(dict.fromkeys(allposts))

    site = Main.objects.get(pk=2)
    posts = Posts.objects.filter(act=1).order_by('-pk')
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    lastposts = Posts.objects.filter(act=1).order_by('-pk')[:3]
    popularposts = Posts.objects.filter(act=1).order_by('-views')
    popularposts2 = Posts.objects.filter(act=1).order_by('-views')[:3]
    lastposts2 = Posts.objects.filter(act=1).order_by('-pk')[:4]

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)

    today = str(year) + "/" + str(month) + "/" + str(day)

    f_rom = []
    t_o = []

    for i in range(30):

        b = datetime.datetime.now() - datetime.timedelta(days=i)

        year = b.year
        month = b.month
        day = b.day

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)
        
        b = str(year) + "/" + str(month) + "/" + str(day)

        f_rom.append(b)

    for i in range(30):
    
        b = datetime.datetime.now() - datetime.timedelta(days=i)

        year = b.year
        month = b.month
        day = b.day

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)
        
        b = str(year) + "/" + str(month) + "/" + str(day)

        t_o.append(b)

    return render(request, 'front/all_posts_full.html', {'site':site, 'posts':posts, 'category':category, 'subcategory':subcategory, 'lastposts':lastposts, 'popularposts':popularposts, 'popularposts2':popularposts2, 'lastposts2':lastposts2, 'allposts':allposts, 'f_rom':f_rom, 't_o':t_o})