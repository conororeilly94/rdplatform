from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls), # Admin page
    url(r'', include('main.urls')), # Root
    url(r'', include('posts.urls')), # Posts page
    url(r'', include('category.urls')), # Categories
    url(r'', include('subcategory.urls')), # Subctegories
    url(r'', include('contactform.urls')), # Contact Form
    url(r'', include('manager.urls')), # Manager Form
    url(r'', include('newsletter.urls')),
    url(r'', include('comment.urls')),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)