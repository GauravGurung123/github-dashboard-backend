from django.contrib.auth import get_user_model
from rest_framework import serializers
# from .models import UserProfile
from accounts.models import UserProfile
User = get_user_model()


class UserCreateRequestsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'phone_number', 'address')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', validated_data.pop('password', None))

        user = User.objects.create_user(**user_data, password=password)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            if attr == 'password':
                user.set_password(value)
            else:
                setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = instance.user.id
        return rep
    
class UserCreateRequestsSerializer_(serializers.ModelSerializer) :
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone_number', 'address')
    
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value
    
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        phone_number = validated_data.get('phone_number', '')
        address = validated_data.get('address', '')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            address=address
        )
        
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
            
        instance.save()
        
        profile = instance.userprofile
        profile.phone_number = validated_data.get('phone_number', profile.phone_number)
        profile.address = validated_data.get('address', profile.address)
        profile.save()
        
        return instance