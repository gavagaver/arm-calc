from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calc/', include('calc.urls', namespace='calc')),
    path('account/', include('account.urls', namespace='account')),
]
