from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('brands/', include('brands.urls')),
    path('categories/', include('categories.urls')),
    path('products/', include('products.urls')),
    path('inflows/', include('inflows.urls')),
    path('outflows/', include('outflows.urls')),
]
