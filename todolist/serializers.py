from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Todo
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class TodoSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Todo
        fields = [
            'id',
            'owner_username',
            'title',
            'description',
            'is_completed',
            'due_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner_username', 'created_at', 'updated_at']

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError("Passwords don't match")
        password_validation.validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
