from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import transaction

from .models import Product, Cart, CartItem, Order, OrderItem


def product_list(request):
    """Show all products on the homepage."""
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, pk):
    """Show a single product's details."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def register(request):
    """User registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('product_list')


@login_required
def add_to_cart(request, pk):
    """Add a product to the logged-in user's cart, or increase quantity if already there."""
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        item.quantity += 1
        item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect('product_list')


@login_required
def view_cart(request):
    """Show all items currently in the user's cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
def update_cart_item(request, item_id):
    """Update quantity or remove an item from the cart."""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            item.quantity += 1
            item.save()
        elif action == 'decrease':
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
        elif action == 'remove':
            item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    """Convert the current cart into an Order, then empty the cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')

    with transaction.atomic():
        order = Order.objects.create(user=request.user, total_amount=cart.total_price())
        for cart_item in items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price_at_purchase=cart_item.product.price,
            )
        items.delete()  # empty the cart after order is placed

    messages.success(request, f"Order #{order.id} placed successfully!")
    return redirect('order_detail', pk=order.id)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})
