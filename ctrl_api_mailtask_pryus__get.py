import json

from django.http import HttpResponse
from rest_framework.response import Response
from YBWEB.ctxJSON import DICTJSON, templateCTX

from models.flgesttare.gt_tareas import gt_tareas as tareas


# @class_declaration interna_get #
class interna_get():
    pass


# @class_declaration diagnosis_get #
class diagnosis_get(interna_get):

    @staticmethod
    def start(pk, data):
        response = ""
        status = 200
        pryus = tareas.getpryus(data["appid"], data["email"])
        if "error" in pryus:
            response = json.dumps(pryus)
            status = 400
        else:
            # response = DICTJSON.toJSON(pryus)
            response = json.dumps(pryus)

        return HttpResponse(response, status=status, content_type="application/json")


# @class_declaration get #
class get(diagnosis_get):
    pass
