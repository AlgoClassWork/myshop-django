"""
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from store.views import product_list, product_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    # http://127.0.0.1:8000/ главная 
    path('', product_list, name='product_list'),
    # http://127.0.0.1:8000/category/3 например электроника
    path('category/<int:category_id>/', product_list, name='category_products'),
    # http://127.0.0.1:8000/product/1 например Iphone 15
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
