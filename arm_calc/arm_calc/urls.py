from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('calc/', include('calc.urls', namespace='calc')),
    path('', include('account.urls', namespace='account')),
]
