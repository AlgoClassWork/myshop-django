from django.shortcuts import render, get_object_or_404

from store.models import Product, Category

# Create your views here.
# http://127.0.0.1:8000/ главная
# http://127.0.0.1:8000/category/3 например электроника
def product_list(request, category_id=None):
    products = Product.objects.all()
    categories = Category.objects.all()

    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=selected_category)

    return render(request, 'product_list.html', 
    {'products' : products, 'categories' : categories})

# http://127.0.0.1:8000/product/1 например Iphone 15
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html',
    {'product': product})