from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import *

router=DefaultRouter()

router.register('list',UserApiView,basename='user')
router.register('jobs', JobPostViewSet,basename='jobs')


urlpatterns = [
    path('',include(router.urls)),
    path("register/", UserRegistrationApiView.as_view(), name="register"),
    path("login/", UserLoginApiView.as_view(), name="login"),
    path('logout/',UserLogoutApiView.as_view(),name='logout'),
    path("active/<uid64>/<token>/",activate,name='activate'),


    
    
]