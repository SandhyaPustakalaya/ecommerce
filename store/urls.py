from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('track_order/', views.track_order, name='track_order'),
    path('pay/', views.payment_page, name='payment_page'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('profile/', views.profile_view, name='profile'),
    path('my_account/', views.my_account, name='my_account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
     path('wishlist/', views.view_wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('secret-admin/', admin.site.urls), 
]

urlpatterns += [
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='/my_account/'
    ), name='change_password'),
]