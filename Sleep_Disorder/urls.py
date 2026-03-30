"""Sleep_Disorder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from users import views as UserView
from admins import views
from users.utility import training_model
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserView.Index, name='index'),

    path('adminLogin/', views.AdminLogin, name='adminLogin'),
    path('adminlogout/', views.AdminLogout, name='adminlogout'),
    path('adminhome/',views.AdminHome, name='adminhome'),


    path('activatedusers/', views.ActivatedUsers, name='activateduser'),
    path('useractivate/<int:pk>', views.UserActivate, name='useractivate'),
    path('Blockuser/<int:pk>', views.BlockUser, name='blockuser'),

    path('modelEvaluation/', training_model.Model_Evaluation_View, name='modeleval'),
    path('modelprediction/', training_model.ModelPrediction, name='modelprediction'),

    path('userLogin/', UserView.UserLoginPage, name='userLogin'),
    path('userlogout/', UserView.UserLogout, name='userLogout'),
    path('UserRegister/', UserView.UserRegistrationPage, name='userregister'),

    path('UserHome/', UserView.UserHomePage, name='UserHome'),
    path('datasetview/', UserView.DataSetView, name='datasetview'),
    path('matrices/', UserView.ModelMatrices, name='modelmatrices'),

    path('about/', UserView.About, name='about'),

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
