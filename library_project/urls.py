from django.contrib import admin
from django.contrib.auth import views as auth_views
from books import views as book_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        '',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            redirect_authenticated_user=False,
        ),
        name='login',
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            redirect_authenticated_user=False,
        ),
        name='login',
    ),
    path('register/', book_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('books.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
