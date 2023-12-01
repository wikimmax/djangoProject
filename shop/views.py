from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, get_object_or_404, render
from .models import Product, Cart, Order, OrderItem
from .forms import SignUpForm


def index(request):
    return render(request, 'index.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product, defaults={'quantity': 0})
    cart.quantity += 1
    cart.save()
    return redirect('product_list')


def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})


def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if cart_items.exists():
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart_items.delete()
        return redirect('order_detail', pk=order.pk)
    return redirect('cart_detail')


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


def payment_page(request):
    return render(request, 'payment_page.html')


def process_payment(request):
    if request.method == 'POST':
        blik_code = request.POST.get('blik_code')
        if validate_blik_code(blik_code):
            return place_order(request)
        else:
            return redirect('payment_page')  # Include error message context


def validate_blik_code(code):
    # Simulate BLIK code validation
    return len(code) == 6 and code.isdigit()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to a home page or another appropriate page
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    if request.method == 'POST':
        cart_item.delete()
        return redirect('cart_detail')


@login_required
def browse_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'browse_orders.html', {'orders': orders})
