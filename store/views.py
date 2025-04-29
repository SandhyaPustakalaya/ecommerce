from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .forms import RegisterForm
from .models import Product, Cart
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Order
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import EditProfileForm
from django.urls import path
from . import views

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # --- Header ---
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "Sandhya Pustakalaya")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 70, "Dharma, Midnapore")
    p.drawString(50, height - 85, "Phone: 7602677933")
    p.drawString(50, height - 100, "Email: chiranjitsenapati.mdn@gmail.com")

    # --- Invoice Title ---
    p.setFont("Helvetica-Bold", 16)
    p.drawString(400, height - 50, f"INVOICE")
    p.setFont("Helvetica", 12)
    p.drawString(400, height - 70, f"Order ID: #{order.id}")
    p.drawString(400, height - 85, f"Status: {order.status}")
    p.drawString(400, height - 100, f"Date: {order.ordered_at.strftime('%d-%m-%Y')}")

    # --- Line separator ---
    p.line(50, height - 110, 550, height - 110)

    # --- Billing Info ---
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 140, "Billing Details:")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 160, f"Customer: {order.user.username}")
    p.drawString(50, height - 175, f"Phone: {order.phone}")
    p.drawString(50, height - 190, f"Address: {order.address}")

    # --- Product Info ---
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 220, "Product Summary:")
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 240, "Product")
    p.drawString(250, height - 240, "Qty")
    p.drawString(300, height - 240, "Price")
    p.drawString(400, height - 240, "Total")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 260, order.product.title)
    p.drawString(250, height - 260, str(order.quantity))
    p.drawString(300, height - 260, f"₹{order.product.price}")
    total = order.quantity * order.product.price
    p.drawString(400, height - 260, f"₹{total}")

    # --- Grand Total ---
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 300, "Grand Total:")
    p.drawString(400, height - 300, f"₹{total}")

    # --- Footer ---
    p.setFont("Helvetica", 10)
    p.drawString(50, 60, "Thank you for shopping with Sandhya Pustakalaya.")
    p.drawString(50, 45, "This is a system-generated invoice and does not require a signature.")

    p.showPage()
    p.save()

    return response


# Home Page View
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to homepage after login
    return render(request, 'login.html')

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

# Add to Cart View
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

# Cart View (Display user-specific cart)
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

from .models import Order

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                address=address,
                phone=phone
            )
        cart_items.delete()
        return redirect('my_orders')
    
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'my_orders.html', {'orders': orders})

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'place_order.html', {'cart_items': cart_items, 'total_price': total_price})

def track_order(request):
    order = None
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        phone = request.POST.get('phone')

        try:
            order = Order.objects.get(id=order_id, phone=phone)
        except Order.DoesNotExist:
            messages.error(request, "❌ Invalid Order ID or Phone number.")

    return render(request, 'track_order.html', {'order': order})

def payment_page(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # For demo, fixed price (can use cart total in real use)
    order_amount = 50000  # ₹500 (in paise)
    order_currency = 'INR'

    razorpay_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture='1'))

    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': order_amount,
        'currency': order_currency,
    }
    return render(request, 'payment_page.html', context)

def product_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(title__icontains=query)
    if category and category != "All":
        products = products.filter(category=category)

    categories = Product.CATEGORY_CHOICES

    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    order_amount = int(total_price * 100)  # Convert to paise

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create(dict(amount=order_amount, currency='INR', payment_capture='1'))

    request.session['razorpay_order_id'] = razorpay_order['id']

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'currency': 'INR',
    })

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        # Optional: Add signature verification here

        # Update orders with this razorpay_order_id
        orders = Order.objects.filter(user=request.user, status="Pending", razorpay_order_id__isnull=True)

        for order in orders:
            order.razorpay_order_id = razorpay_order_id
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.status = "Confirmed"
            order.save()

        return render(request, 'payment_success.html')

    return redirect('home')

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})

@login_required
def my_account(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-ordered_at')

    return render(request, 'my_account.html', {
        'user': user,
        'orders': orders
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profile updated successfully.")
            return redirect('my_account')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def profile(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)
    return render(request, 'profile.html', {'orders': orders})

@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist.objects.create(user=request.user, product=product)
    return redirect('wishlist')  # Redirect after adding to wishlist

@login_required
def view_wishlist(request):
    wishlist_items = wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
