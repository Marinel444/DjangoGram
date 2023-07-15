from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from gramm.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_post/', add_post, name='add_post'),
    path('profile/', profile_user, name='profile'),
    path('account/<int:user_id>/', account_user, name='account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
