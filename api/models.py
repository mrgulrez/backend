
# from django.db import models

# class Message(models.Model):
#     name = models.CharField(max_length=100)
#     text = models.TextField()

#     def __str__(self):
#         return f"{self.name}: {self.text[:30]}"

# class Build(models.Model):
#     build_id = models.CharField(max_length=50, unique=True)
#     frame = models.CharField(max_length=100)
#     propellers = models.CharField(max_length=100, blank=True, null=True)
#     motors = models.CharField(max_length=100, blank=True, null=True)
#     battery = models.CharField(max_length=100, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.build_id









from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.text[:30]}"

class Build(models.Model):
    name = models.CharField(max_length=100)
    build_id = models.CharField(max_length=50, unique=True)
    frame = models.CharField(max_length=100)
    camera = models.CharField(max_length=100, blank=True, null=True)
    propellers = models.CharField(max_length=100, blank=True, null=True)
    motors = models.CharField(max_length=100, blank=True, null=True)
    vtx = models.CharField(max_length=100, blank=True, null=True)
    battery = models.CharField(max_length=100, blank=True, null=True)
    expected_delivery_date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.build_id

class DeliveryDetails(models.Model):
    #build = models.OneToOneField(Build, on_delete=models.CASCADE, related_name='delivery')
    delivery_id = models.CharField(max_length=50, unique=True)
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