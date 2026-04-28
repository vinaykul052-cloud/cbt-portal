from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    #path('', lambda request: redirect('login')),  # default login page
    path('admin/', admin.site.urls),
    path('', include('exam.urls')),  # सारी routing exam app handle करेगा
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)