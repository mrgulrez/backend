from django.contrib import admin
from .models import Order, Build, Message, Coupon

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'shipment_id', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_id', 'shipment_id')
    readonly_fields = ('order_id', 'created_at', 'updated_at', 'build_snapshot', 'delivery_snapshot')
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'status', 'created_at', 'updated_at')
        }),
        ('Tracking Information', {
            'fields': ('shipment_id', 'tracking_url')
        }),
        ('Order Details', {
            'fields': ('build_snapshot', 'delivery_snapshot'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Automatically update status when shipment info is added
        if obj.shipment_id and obj.tracking_url and obj.status != 'dispatched':
            obj.status = 'dispatched'
        super().save_model(request, obj, form, change)



admin.site.register(Coupon)


