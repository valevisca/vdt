"""vdt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vdt_design import views
# This import is required to access MEDIA_URL and MEDIA_ROOT
from django.conf import settings
# To manage static objects, like images, we need to imprort the static module
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('password/', views.change_password, name='change_password'),

    # Design
    path('', views.home, name='home'),
    path('designs/', views.currentdesigns, name='currentdesigns'),
    path('upload/', views.upload, name='upload'),
    path('designs/upload/', views.designupload, name='designupload'),
    path('designs/<int:design_pk>', views.viewdesign, name='viewdesign'),
    path('designs/<int:design_pk>/delete', views.deletedesign, name='deletedesign'),
    path('designs/<int:design_pk>/analyse', views.analysedesign, name='analysedesign'),

]

# The following code is required in order to serve media files/static files on Django
# development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
