from rest_framework import status
from django.contrib.sessions.models import Session
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.serializers import UserSerializer
from datetime import datetime
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache 

class Login(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {'request': request})
        print(request)
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user = user)
                user_serializer = UserSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Start session success'                        
                    }, status = status.HTTP_201_CREATED)
                else:
                    # all_sessions = Session.objects.filter(expire_date = datetime.now)
                    # if all_sessions.exists():
                    #     for session in all_sessions:
                    #         session_data = session.get_decoded()
                    #         if user.id == int(session_data.get('_auth_user_id')):
                    #             session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Start session success'                        
                    }, status = status.HTTP_201_CREATED)
            else:
                return Response({'error':'este usuario no puede iniciar sesion'}, status = status.HTTP_401_UNAUTHORIZED)        
        else:
            return Response({'mensaje':'user o password incorrectos'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'hola desde response'}, status = status.HTTP_200_OK)

