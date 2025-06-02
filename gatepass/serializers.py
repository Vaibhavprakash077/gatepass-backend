from rest_framework import serializers
from django.contrib.auth.models import User
from .models import GatePass, UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True, required=False, default='student')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
    
    def create(self, validated_data):
        role = validated_data.pop('role', 'student')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # UserProfile is created automatically via signal
        user.userprofile.role = role
        user.userprofile.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='userprofile.role', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class GatePassSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    
    class Meta:
        model = GatePass
        fields = [
            'id',
            'user_id', 
            'student_name',
            'roll_number',
            'department',
            'material_description',
            'date_time',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'user_id', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class GatePassUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatePass
        fields = ['status']
    
    def update(self, instance, validated_data):
        if validated_data.get('status') in ['approved', 'rejected']:
            instance.approved_by = self.context['request'].user
        return super().update(instance, validated_data)