from django.contrib import admin
from .models import Product, Cart, Order
from django.core.mail import send_mail

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'status', 'ordered_at']
    list_filter = ['status', 'ordered_at']
    search_fields = ['user__username', 'product__title']
    list_editable = ['status']  # ✅ Admin can change status directly
    ordering = ['-ordered_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']

def save_model(self, request, obj, form, change):
        if change:
            old_order = Order.objects.get(pk=obj.pk)
            if old_order.status != obj.status:
                # Send email
                send_mail(
                    subject='Your Order Status has been Updated',
                    message=f"Hi {obj.user.username}, your order for '{obj.product.title}' is now marked as **{obj.status}**.",
                    from_email='no-reply@sandhyapustakalaya.com',
                    recipient_list=[obj.user.email],
                    fail_silently=True,
                )
        super().save_model(request, obj, form, change)
