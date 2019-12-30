# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from rest_framework.response import Response

from models.flgesttare.gt_tareas import gt_tareas as tareas


# @class_declaration interna_create #
class interna_create():
    pass


# @class_declaration diagnosis_create #
class diagnosis_create(interna_create):

    @staticmethod
    def start(pk, data):
        response = tareas.createinbox(data)
        status = 200
        if "error" in response:
            response = json.dumps(response)
            status = 400
        else:
            response = json.dumps(response)
        
        return HttpResponse(response, status=status, content_type="application/json")


# @class_declaration create #
class create(diagnosis_create):
    pass
