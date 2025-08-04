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
from .models import Message, Build, DeliveryDetails

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



class OrderSerializer(serializers.ModelSerializer):
   # track_status = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'order_id', 
            'created_at', 
            'updated_at', 
            'build_snapshot', 
            'delivery_snapshot',
            'status_history'
        ]


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