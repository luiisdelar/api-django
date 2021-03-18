# debes importar tu modelo de usuario, independiente de cual sea
from api.models import User

class UserAuthentificacionBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            # en este punto, debes verificar la contraseña, yo lo hare como lo hace el modelo de usuario de django, siguiendo los metodos que trae este
            if user.password == password:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except:
            return None
