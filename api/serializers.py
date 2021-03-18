from rest_framework import serializers
from .models import User, Rol
from django.contrib.auth.models import Group
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    class Meta:
        model = User
        fields = '__all__'
    

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            rol=validated_data['rol'],
        )
        
        if User.objects.filter(username=validated_data['username']):
            raise serializers.ValidationError('This username already exist.')
        
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user_old = User.objects.filter(username=validated_data['username']).first()
        if user_old and user_old.id != instance.id:
            raise serializers.ValidationError('This username already exist.')
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.rol = validated_data.get('rol', instance.rol)
        user_oldd = User.objects.filter(email=validated_data['email']).first()
        
        if user_oldd and user_oldd.id != instance.id:
            raise serializers.ValidationError('This email already exist.')
        
        instance.email = validated_data['email']
        instance.save()   
        return instance

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

    def create(self, validated_data):
        rol = Rol(**validated_data)
        if Rol.objects.filter(name=validated_data['name']):
            raise serializers.ValidationError('This rol name already exist.')
        rol.save()
        return rol   

    def update(self, instance, validated_data):
        rol_old = Rol.objects.filter(name=validated_data['name']).first()
        if rol_old and rol_old.id != instance.id:
            raise serializers.ValidationError('This rol name already exist.')
        instance.name = validated_data.get('name', instance.name)
        instance.save()   
        return instance