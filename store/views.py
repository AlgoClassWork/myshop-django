from django.shortcuts import render, get_object_or_404, redirect

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

# http://127.0.0.1:8000/cart Просмотр корзины
def cart(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    return render(request, 'cart.html', 
    {'products': products})

# http://127.0.0.1:8000/cart/add/2 Добавить Iphone 16
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
        request.session['cart'] = cart
    return redirect('cart')

# http://127.0.0.1:8000/cart/remove/3 Удалить Бетмена
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        request.session['cart'] = cart
    return redirect('cart')