from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('user/', include('apps.user.urls', namespace='user')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('basket/', include('apps.basket.urls', namespace='basket')),
    path('checkout/', include('apps.checkout.urls')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('crash/', views.crash_view, name='crash'), #for testing 500 page
    path('test404/', views.test_404_template), #for testing 404 page
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "config.views.error_404"
handler500 = "config.views.error_500"
