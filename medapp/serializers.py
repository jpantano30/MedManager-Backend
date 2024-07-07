from rest_framework import serializers
from .models import Medication, MedicationLog, User
from django.contrib.auth.models import User

class MedicationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    end_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False, allow_null=True)
    refill_due_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False, allow_null=True)
    
    class Meta:
        model = Medication
        fields = ['id', 'name', 'dosage', 'frequency', 'start_date', 'end_date', 'refill_due_date', 'taken', 'user']

class MedicationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationLog
        fields = ['id', 'user', 'medication', 'date', 'taken']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    