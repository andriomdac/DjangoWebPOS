from django.contrib import admin
from django.urls import path, include
from .utils import toggle_theme

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('login.urls')),
    path('', include('home.urls')),
    path('brands/', include('brands.urls')),
    path('categories/', include('categories.urls')),
    path('products/', include('products.urls')),
    path('inflows/', include('inflows.urls')),
    path('outflows/', include('outflows.urls')),
    path('sales/', include('sales.urls')),
    path('theme/', toggle_theme, name='toggle_theme'),
]
