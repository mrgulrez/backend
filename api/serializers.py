# from rest_framework import serializers
# from .models import Build

# class BuildIdSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Build
#         fields = ['build_id']

# class BuildSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Build
#         fields = ['build_id', 'frame', 'propellers', 'motors', 'battery']






from rest_framework import serializers
from .models import Message, Build, DeliveryDetails, Coupon

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'name', 'text', 'created_at']

class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = '__all__'
        read_only_fields = ['build_id', 'created_at', 'updated_at']

class DeliveryDetailsSerializer(serializers.ModelSerializer):
    build_id = serializers.CharField(source='build.build_id', read_only=True)

    class Meta:
        model = DeliveryDetails
        fields = '__all__'
        read_only_fields = ['delivery_id', 'created_at', 'updated_at']

class BuildDetailSerializer(BuildSerializer):
    delivery = DeliveryDetailsSerializer(read_only=True)




from rest_framework import serializers
from .models import Order, Payment

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
#         read_only_fields = ['order_id', 'created_at', 'updated_at', 'status']



class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Coupon
        fields = '__all__'
        read_only_fields = ['used_count', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Create coupon instance
        return Coupon.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Update coupon instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class OrderSerializer(serializers.ModelSerializer):
   # track_status = serializers.CharField(source='get_status_display', read_only=True)
    coupon = CouponSerializer(read_only=True)
    coupon_code = serializers.CharField(
        write_only=True,
        required=False, 
        allow_null = True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'order_id', 
            'created_at', 
            'updated_at', 
            'build_snapshot', 
            'delivery_snapshot',
            'status_history',
            'coupon',
            'discount_amount'
        ]
    
    def create(self, validated_data):
        coupon_code = validated_data.pop('coupon_code', None)

    
    def validate_coupon_code(self, value):
        if value:
            try:
                coupon = Coupon.objects.get(code=value)
                if not coupon.is_valid():
                    raise serializers.ValidationError("Coupon is invalid or expired")
            except Coupon.DoesNotExist:
                raise serializers.ValidationError("Invalid coupon code")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = [
            'payment_id', 
            'created_at', 
            'updated_at',
            'status'
        ]