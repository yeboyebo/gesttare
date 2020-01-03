
# @class_declaration gesttare #
from django.http import HttpResponse
import json
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


class gesttare(yblogin_sass):

    def gesttare_forbiddenError(self, request):
        return HttpResponseRedirect("/gesttare/gt_tareas/custom/denegado")

    def gesttare_token_auth(self, request):
        try:
            params = json.loads(request.body.decode("utf-8"))
            username = params["username"]
            password = params["password"]

        except Exception:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)


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

    @csrf_exempt
    def token_auth(self, request):
        return self.iface.gesttare_token_auth(request)

    def gesttare_login(self, request, error=None):
        redirect_uri = request.GET.get("redirect_uri", None)
        state = request.GET.get("state", None)
        if request.user.is_authenticated():
            if redirect_uri and redirect_uri != None and redirect_uri != "None":
                email = qsatype.FLUtil.sqlSelect(u"aqn_user", u"email", u"idusuario = '" + str(request.user.username) + u"'")
                url = redirect_uri + "?state=" + state + "&code=" + str(email) + "&token=prueba"
                return HttpResponseRedirect(url)
        if not error:
            error = ""
        return render(request, "portal/login.html", {"error": error, "redirect_uri": redirect_uri, "state": state})

    def login(self, request, error=None):
        return self.iface.gesttare_login(request, error)

    def gesttare_auth_login(self, request):
        if request.method == "POST":
            action = request.POST.get("action", None)
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            redirect_uri = None
            state = None
            try:
                redirect_uri = request.POST.get("redirect_uri", None)
                state = request.POST.get("state", None)
                print(redirect_uri, "    ", state)
            except Exception as e:
                print(e)

            if action == "login":
                if username == "admin":
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login_auth(request, user)
                        accessControl.accessControl.registraAC()
                    else:
                        return self.iface.login(request, 'Error de autentificación')
                    return HttpResponseRedirect("/")

                usuario = aqn_user.objects.filter(email__exact=username)
                if len(usuario) == 0:
                    return self.iface.login(request, 'No existe el usuario')
                if usuario[0].activo is False:
                    return self.iface.login(request, 'No existe el usuario')
                md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                # print("falla por aqui??", md5passwd, usuario[0].password)
                if usuario[0].password != md5passwd:
                    return self.iface.login(request, 'Error de autentificación')
                idusuario = usuario[0].idusuario
                user = authenticate(username=idusuario, password="ybllogin")
                if user is not None:
                    login_auth(request, user)
                else:
                    return self.iface.login(request, "Error de autentificación")
                accessControl.accessControl.registraAC()
                if redirect_uri and redirect_uri != None and redirect_uri != "None":
                    url = redirect_uri + "?state=" + state + "&code=" + username + "&token=prueba"
                    return HttpResponseRedirect(url)
                return HttpResponseRedirect("/")
        return self.iface.login(request)

    def auth_login(self, request):
        return self.iface.gesttare_auth_login(request)

