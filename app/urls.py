from django.contrib import admin
from django.urls import path, include
from .utils import toggle_theme, toggle_sidebar
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('login.urls')),
    path('', include('webstore.urls')),
    path('dashboard/', include('home.urls')),
    path('products/', include('products.urls')),
    path('categories/', include('categories.urls')),
    path('inflows/', include('inflows.urls')),
    path('outflows/', include('outflows.urls')),
    path('sales/', include('sales.urls')),
    path('orders/', include('orders.urls')),

    path('theme/toggle_theme/', toggle_theme, name='toggle_theme'),
    path('theme/toggle_sidebar/', toggle_sidebar, name='toggle_sidebar')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
