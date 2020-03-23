
# @class_declaration gesttare #
from django.http import HttpResponse
import json
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from YBUTILS.APIQSA import APIQSA


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

        # Comprobamos usuario con pineboo
        try:
            authusername = APIQSA.login(username, password)
            if authusername:
                user = User.objects.filter(username=str(authusername))
                if user.exists():
                    authuser = authenticate(username=str(authusername), password=password)
                    if authuser is None:
                        user = User.objects.get(username__exact=str(authusername))
                        user.set_password(password)
                        user.save()
                        authuser = authenticate(username=str(authusername), password=password)
                else:
                    user = User.objects.create_user(username=str(authusername), password=password)
                    user.is_staff = False
                    user.save()
                    authuser = authenticate(username=str(authusername), password=password)
                token, _ = Token.objects.get_or_create(user=authuser)
                resul = HttpResponse(json.dumps({'token': token.key}), status=200)
        except Exception as e:
            print("-----------------------")
            print(e)
            resul = HttpResponse(json.dumps({'error': str(e)}), status=404)
        resul['Access-Control-Allow-Origin'] = '*'
        return resul
        # try:
        #     params = json.loads(request.body.decode("utf-8"))
        #     username = params["username"]
        #     password = params["password"]

        # except Exception:
        #     username = request.POST.get("username", None)
        #     password = request.POST.get("password", None)


        # usuario = aqn_user.objects.filter(email__exact=username)
        # if len(usuario) == 0:
        #     return HttpResponse(json.dumps({'error': 'No existe el usuario'}),
        #                     status=404)
        # if usuario[0].activo is False:
        #     return HttpResponse(json.dumps({'error': 'No existe el usuario'}),
        #                     status=404)
        # md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
        # if usuario[0].password != md5passwd:
        #     return HttpResponse(json.dumps({'error': 'Contraseña invalida'}),
        #                     status=404)
        # idusuario = usuario[0].idusuario
        # user = authenticate(username=idusuario, password="ybllogin")
        # if not user:
        #     return HttpResponse(json.dumps({'error': 'Usuario y contraseña no coinciden'}),
        #                     status=404)
        # token, _ = Token.objects.get_or_create(user=user)

        # return HttpResponse(json.dumps({'token': token.key}), status=200)

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
        if not error:
            error = ""
        if request.user.is_authenticated():
            if redirect_uri and redirect_uri != None and redirect_uri != "None":
                return render(request, "portal/login.html", {"error": error, "redirect_uri": redirect_uri, "state": state})
                # email = qsatype.FLUtil.sqlSelect(u"aqn_user", u"email", u"idusuario = '" + str(request.user.username) + u"'")
                # url = redirect_uri + "?state=" + state + "&code=" + str(email) + "&token=prueba"
                # return HttpResponseRedirect(url)
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
                try:
                    authusername = APIQSA.login(username, password)
                    if authusername:
                        id_usuario = qsatype.FLUtil.sqlSelect("aqn_user", "idusuario", "email = '" + str(username) + "'")
                        ultimo_login = qsatype.FLUtil.sqlSelect("auth_user", "last_login", "username = '" + str(id_usuario) + "'")
                        if ultimo_login is None:
                            APIQSA.entry_point('post', "aqn_companies", "", str(username), "enviar_wiki")
                        # APIQSA.entry_point('post', "aqn_companies", "", "", "enviar_wiki")
                        usuario = aqn_user.objects.filter(email__exact=username)
                        if usuario.exists():
                            authuser = authenticate(username=str(authusername), password=password)
                            if authuser is None:
                                user = User.objects.get(username__exact=str(authusername))
                                user.set_password(password)
                                user.save()
                                authuser = authenticate(username=str(authusername), password=password)
                        else:
                            usuario = User.objects.create_user(username=str(authusername), password=password)
                            usuario.is_staff = False
                            usuario.save()
                            authuser = authenticate(username=str(authusername), password=password)

                        # if len(usuario) == 0:
                        #     return self.iface.login(request, 'No existe el usuario')
                        # if usuario[0].activo is False:
                        #     return self.iface.login(request, 'No existe el usuario')
                        # md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                        # # print("falla por aqui??", md5passwd, usuario[0].password)
                        # if usuario[0].password != md5passwd:
                        #     return self.iface.login(request, 'Error de autentificación')
                        idusuario = authusername
                        if redirect_uri and redirect_uri != None and redirect_uri != "None":
                            url = redirect_uri + "?state=" + state + "&code=" + username + "&token=prueba"
                            return HttpResponseRedirect(url)
                        # user = authenticate(username=idusuario, password="ybllogin")
                        if authuser is not None:
                            login_auth(request, authuser)
                        else:
                            return self.iface.login(request, "Error de autentificación")
                        accessControl.accessControl.registraAC()
                        return HttpResponseRedirect("/")
                    else:
                        return self.iface.login(request, 'No existe el usuario')
                except Exception as e:
                    return self.iface.login(request, str(e))
        return self.iface.login(request)

    def gesttare_erroractivecompany_request(self, request, hashparam):
        return self.iface.erroractivecompany(request)

    def gesttare_emailenviado_request(self, request, hashparam):

        if request.method == "POST":
            action = request.POST.get("action", None)

            if action == "reenviaremail":

                email = qsatype.FLUtil.sqlSelect("aqn_invitations", "email", "hashcode = '" + str(hashparam) + u"'")
                id_compania = qsatype.FLUtil.sqlSelect("aqn_invitations", "idcompany", "hashcode = '" + str(hashparam) + u"'")

                params = {
                    "email": email,
                    "hashcode": hashparam,
                    "id_compania": id_compania
                }
                APIQSA.entry_point('post', "aqn_companies", "", params, "reenviar")
        return self.iface.emailenviado(request, hashparam)

    def gesttare_emailreenviado_request(self, request):
        return self.iface.emailreenviado(request)

    def gesttare_activecompany_request(self, request, hashparam):

        # API.sdsd(hashparam)
        cursor = qsatype.FLSqlCursor(u"aqn_invitations")
        cursor.select("hashcode = '{}'".format(hashparam))
        if not cursor.first():
            return HttpResponseRedirect("/403")
        cursor.setModeAccess(cursor.Browse)
        cursor.refreshBuffer()
        email = cursor.valueBuffer("email")
        id_company = cursor.valueBuffer("idcompany")
        params = {
            "email": email,
            "id_company": id_company
        }
        # idinvitation = cursor.valueBuffer("id")
        # Activamos compañia la damos por validada y activamos el usuario
        if not APIQSA.entry_point('post', "aqn_companies", "", params, 'validar'):
            return False
            # return self.iface.error_activar(request)


        return self.iface.activecompany(request)

    def gesttare_newcompany_request(self, request):
        if request.method == "POST":
            action = request.POST.get("action", None)
            username = request.POST.get("username", None)
            nombre = request.POST.get("nombre", None)
            email = request.POST.get("email", None)
            apellidos = request.POST.get("apellidos", None)
            password = request.POST.get("password", None)
            password2 = request.POST.get("password2", None)
            nombre_company = request.POST.get("nombrecompany", None)
            descripcion = request.POST.get("planes", None)
            modalidad = request.POST.get("modalidad", None)

            # if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', email.lower()):
            #     return self.iface.newcompany(request, email, "El email no tiene el formato correcto")
            if action == "newcompany":
                id_plan = qsatype.FLUtil.sqlSelect("aqn_planes", "idplan", "descripcion = '" + str(descripcion) + "' AND modalidad = '" + str(modalidad) + "'")
                params = {
                    'nombre': nombre_company,
                    "idplan": id_plan,
                    "descripcion": nombre_company,
                    "usuario": {
                        'email': email,
                        'usuario': username,
                        'nombre': nombre,
                        'apellidos': apellidos,
                        'password': password,
                        'password2': password2,
                    }
                }
                try:
                    resultado = APIQSA.entry_point('post', "aqn_companies", username, params)
                    id_compania = resultado[0]
                    id_usuario = resultado[1]
                    hashcode = resultado[2]
                except Exception as exc:
                    return self.iface.newcompany(request, str(exc))
                if not id_compania:
                    return self.iface.newcompany(request, "Error no se puede crear usuario y compañía")

                user = User.objects.create_user(username=id_usuario, password="ybllogin", first_name=username)
                user.save()
                if not qsatype.FLUtil.sqlUpdate("auth_user", "is_superuser", True, "username = '" + str(id_usuario) + "'"):
                    return False
                # return self.iface.login(request, None, "Bienvenido a dailyjob, es necesario validar email")
                url = "/emailenviado/" + hashcode
                return HttpResponseRedirect(url)

        return self.iface.newcompany(request, "")

    def gesttare_newcompany(self, request, error):
        username = request.POST.get("username", None) or ""
        nombre = request.POST.get("nombre", None) or ""
        apellidos = request.POST.get("apellidos", None) or ""
        nombrecompany = request.POST.get("nombrecompany", None) or ""

        return render(request, "portal/newcompany.html", {"error": error, "nombrecompany":nombrecompany, "nombre": nombre, "apellidos": apellidos, "username": username})

    def gesttare_erroractivecompany(self, request):
        return render(request, "portal/erroractivecompany.html")

    def gesttare_activecompany(self, request):
        return render(request, "portal/activecompany.html")

    def gesttare_emailenviado(self, request, hashparam):
        return render(request, "portal/emailenviado.html", {"hashparam": hashparam})

    def gesttare_emailreenviado(self, request):
        return render(request, "portal/emailreenviado.html")

    def auth_login(self, request):
        return self.iface.gesttare_auth_login(request)

    def newcompany_request(self, request):
        return self.iface.gesttare_newcompany_request(request)

    def newcompany(self, request, error):
        return self.iface.gesttare_newcompany(request, error)

    def activecompany_request(self, request, hashparam):
        return self.iface.gesttare_activecompany_request(request, hashparam)

    def activecompany(self, request):
        return self.iface.gesttare_activecompany(request)

    def erroractivecompany_request(self, request, hashparam):
        return self.iface.gesttare_erroractivecompany_request(request, hashparam)

    def erroractivecompany(self, request):
        return self.iface.gesttare_erroractivecompany(request)

    def emailenviado_request(self, request, hashparam):
        return self.iface.gesttare_emailenviado_request(request, hashparam)

    def emailenviado(self, request, hashparam):
        return self.iface.gesttare_emailenviado(request, hashparam)

    def emailreenviado_request(self, request):
        return self.iface.gesttare_emailreenviado_request(request)

    def emailreenviado(self, request):
        return self.iface.gesttare_emailreenviado(request)

