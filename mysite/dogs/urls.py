from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    # path('', cache_page(60)(DogsHome.as_view()), name='home'),
    path('', DogsHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('adddog/', AddPage.as_view(), name='add_dog'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', DogsCategory.as_view(), name='category'),
]


