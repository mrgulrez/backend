from django.db import models
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError


class Message(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.text[:30]}"


class Build(models.Model):
    name = models.CharField(max_length=100)
    build_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    frame = models.CharField(max_length=100)
    camera = models.CharField(max_length=100, blank=True, null=True)
    propellers = models.CharField(max_length=100, blank=True, null=True)
    motors = models.CharField(max_length=100, blank=True, null=True)
    vtx = models.CharField(max_length=100, blank=True, null=True)
    battery = models.CharField(max_length=100, blank=True, null=True)
    delivery_time = models.IntegerField(default=15)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.build_id

class DeliveryDetails(models.Model):
    delivery_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    receiver_name = models.CharField(max_length=100)
    receiver_mobile = models.CharField(max_length=15)
    receiver_email = models.EmailField()
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery {self.delivery_id} for {self.build_id}"
    



from decimal import Decimal



class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_uses = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        now = timezone.now()
        # Add explicit timezone awareness
        valid_from = timezone.make_aware(self.valid_from) if timezone.is_naive(self.valid_from) else self.valid_from
        valid_to = timezone.make_aware(self.valid_to) if timezone.is_naive(self.valid_to) else self.valid_to
        
        # Add buffer for time comparisons
        return (
            self.active and
            self.used_count < self.max_uses and
            valid_from <= now and
            now <= valid_to + timezone.timedelta(minutes=1)
        )

    def clean(self):
        if self.valid_from and self.valid_to and self.valid_from >= self.valid_to:
            raise ValidationError("Valid From must be before Valid To")
        
    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)
    
    def apply_discount(self, amount):
        if self.discount_type == 'percentage':
            return Decimal(amount) * (1 - self.discount_value / 100)
        return max(0, Decimal(amount) - self.discount_value)
    

    def __str__(self):
        return self.code
    

    

class Order(models.Model):
    STATUS_CHOICES = [
        ('order_pending', 'Order Pending'),
        ('order_received', 'Order Received'),
        ('building', 'Building/Assembling'),
        ('packing', 'Packing'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    build_snapshot = models.JSONField()
    delivery_snapshot = models.JSONField()
    order_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='order_pending')
    shipment_id = models.CharField(max_length=100, blank=True, null=True)
    tracking_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_history = models.JSONField(default=list) 

    coupon = models.ForeignKey(
        Coupon, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )


    constraints = [
            models.UniqueConstraint(
                fields=['coupon'],
                condition=models.Q(coupon__isnull=False),
                name='unique_coupon_per_order'
            )
        ]


    def save(self, *args, **kwargs):
        # Record status changes
        if self.pk:
            original = Order.objects.get(pk=self.pk)
            if original.status != self.status:
                self.status_history.append({
                    'status': self.status,
                    'timestamp': timezone.now().isoformat(),
                    'changed_by': kwargs.get('changed_by', 'system')
                })
        else:
            self.status_history.append({
                'status': self.status,
                'timestamp': timezone.now().isoformat(),
                'changed_by': 'system'
            })
        super().save(*args, **kwargs)


    def __str__(self):
        return self.order_id
    




class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('created', 'Created'),
        ('attempted', 'Attempted'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    payment_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='created')
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.payment_id} for {self.order.order_id}"
    