from rest_framework import serializers
from .models import User, Rol
from rest_framework.validators import UniqueValidator
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    class Meta:
        model = User
        fields = '__all__'
    

    def create(self, validated_data):
        
        if 'rol' in validated_data:
            user = User(
                email=validated_data['email'],
                username=validated_data['username'],
                rol=validated_data['rol'],
            )
        else:
            user = User(
                email=validated_data['email'],
                username=validated_data['username'],
            )

        if User.objects.filter(username=validated_data['username']):
            raise serializers.ValidationError('This username already exist.')
        
        user.user_verified = False
        user.verified_code = get_random_string(length=10)
        user.set_password(validated_data['password'])
        user.save()
        body = 'El codigo de confirmacion de su cuenta es: '+user.verified_code
        email = EmailMessage('Codigo de confirmacion de App Users en Django', body, to=[user.email])
        #email.send()
        
        return user

    def update(self, instance, validated_data):
        user_old = User.objects.get(id=instance.id)
        
        if user_old and user_old.id != instance.id:
            raise serializers.ValidationError('This username already exist.')
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        
        if instance.password != user_old.password:    
            instance.set_password(validated_data['password'])
        
        instance.rol = validated_data.get('rol', instance.rol)
        
        try:
            user_oldd = User.objects.get(email=validated_data['email'])
        except:
            user_oldd = None
        
        
        if user_oldd and user_oldd.id != instance.id:
            raise serializers.ValidationError('This email already exist.')
        
        if validated_data['user_verified']:
            instance.user_verified = True

        instance.email = validated_data['email']
        instance.save()   
        return instance

class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def create(self, validated_data):
        user = User.objects.get(email = validated_data['email'])
        new_pass = get_random_string(length=10)
        user.set_password(new_pass)
        user.save()
        body = 'Su nueva contraseña es: '+new_pass
        email = EmailMessage('Restauración de contraseña', body, to=[user.email])
        #email.send()
        user.save()
        return user

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

    def create(self, validated_data):
        rol = Rol(
            name = validated_data['name']
        )
        if Rol.objects.filter(name=validated_data['name']):
            raise serializers.ValidationError('This rol name already exist.')
        rol.save()
        return rol   

    def update(self, instance, validated_data):
        rol_old = Rol.objects.filter(name=validated_data['name']).first()
        if rol_old and rol_old.id != instance.id:
            raise serializers.ValidationError('This rol name already exist.')
        instance.name = validated_data.get('name', instance.name)
        
        
        instance.permisos.remove(1)
        instance.permisos.remove(2)
        instance.permisos.remove(3)
        instance.permisos.remove(4)
        instance.permisos.remove(5)
        instance.permisos.remove(6)

        for permiso in validated_data['permisos']:
            instance.permisos.add(permiso)
        
        instance.save()   
        return instance

class RolNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'