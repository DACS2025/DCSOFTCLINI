from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('home') if request.user.is_authenticated else redirect('login')),  # Verifica si el usuario está autenticado
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('core/',include('core.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

