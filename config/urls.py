from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('user/', include('apps.user.urls', namespace='user')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/", include("apps.user.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
