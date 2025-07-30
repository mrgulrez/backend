from rest_framework import serializers
from .models import Build

class BuildIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ['build_id']

class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ['build_id', 'frame', 'propellers', 'motors', 'battery']