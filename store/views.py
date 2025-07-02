from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.db import models
from django.db.models import Avg

from store.forms import *
from store.models import *

# Create your views here.
# http://127.0.0.1:8000/ главная
# http://127.0.0.1:8000/category/3 например электроника
def product_list(request, category_id=None):
    products = Product.objects.all().annotate(avg_rating=Avg('rating__score'))
    categories = Category.objects.all()

    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=selected_category)

    #http://127.0.0.1:8000/?sort=rating
    sort = request.GET.get('sort')
    if sort == 'rating':
        products = products.order_by('-avg_rating')
    elif sort == 'price':
        products = products.order_by('price')

    return render(request, 'product_list.html', 
    {'products' : products, 'categories' : categories})

# http://127.0.0.1:8000/product/1 например Iphone 15
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    ratings = Rating.objects.filter(product=product) 
    avg_rating = round(ratings.aggregate(models.Avg('score'))['score__avg'] or 0, 1)

    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(product=product, user=request.user).first()

    comments = product.comments.order_by('-created_at')
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id = product.id)

    return render(request, 'product_detail.html',
    {'product': product, 'avg_rating': avg_rating, 'user_rating': user_rating,
     'comments': comments, 'comment_form': comment_form })

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

# http://127.0.0.1:8000/order/ Оформить заказ
def order(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    if not products:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.products.set(products)
            order.save()
            request.session['cart'] = []
            return render(request,'order_success.html', 
            {'order': order})

    form = OrderForm()
    return render(request, 'order.html',
    {'products': products, 'form': form})


# http://127.0.0.1:8000/register Регистрация
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')

    return render(request, 'register.html',
    {"form": form})

#http://127.0.0.1:8000/rate/4
@login_required
def product_rate(request, product_id):
    if request.method == 'POST':
        score = int(request.POST.get('score'))
        product = get_object_or_404(Product, id=product_id)

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'score': score}
        )
    return redirect('product_detail', product_id=product_id)