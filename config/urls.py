from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('user/', include('apps.user.urls', namespace='user')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/", include("apps.user.urls")),
    path("accounts/logout/", auth_views.LogoutView.as_view(template_name="registration/logged_out.html"), name="logout"),
    path('basket/', include('apps.basket.urls', namespace='basket')),
    path("checkout/", include("apps.checkout.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
