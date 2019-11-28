
# @class_declaration gesttare #
from django.http import HttpResponse
import json
from rest_framework.authtoken.models import Token


class gesttare(yblogin_sass):

    def gesttare_forbiddenError(self, request):
        return HttpResponseRedirect("/gesttare/gt_tareas/custom/denegado")

    def gesttare_token_auth(self, request):
        username = request.GET.get("username", None)
        password = request.GET.get("password", None)

        usuario = aqn_user.objects.filter(email__exact=username)
        if len(usuario) == 0:
            return HttpResponse(json.dumps({'error': 'No existe el usuario'}),
                            status=404)
        if usuario[0].activo is False:
            return HttpResponse(json.dumps({'error': 'No existe el usuario'}),
                            status=404)
        md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
        if usuario[0].password != md5passwd:
            return HttpResponse(json.dumps({'error': 'Contraseña invalida'}),
                            status=404)
        idusuario = usuario[0].idusuario
        user = authenticate(username=idusuario, password="ybllogin")
        if not user:
            return HttpResponse(json.dumps({'error': 'Usuario y contraseña no coinciden'}),
                            status=404)
        token, _ = Token.objects.get_or_create(user=user)

        return HttpResponse(json.dumps({'token': token.key}), status=200)

    def __init__(self, context=None):
        super().__init__(context)

    def forbiddenError(self, request):
        return self.iface.gesttare_forbiddenError(request)

    def token_auth(self, request):
        return self.iface.gesttare_token_auth(request)

