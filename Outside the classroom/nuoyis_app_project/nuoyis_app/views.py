import importlib

from django.shortcuts import render

# Create your views here.
# -- coding: utf-8 --**

import os
import json
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods


def index(request):
    urllist = []
    data = os.listdir("./api")
    for value in data:
        urllist.append(f'path({value}/, views.api_view, name=folder)')
    return HttpResponse(urllist)


def api_view(request, folder_name):
    module_name = f'api.{folder_name}.index'
    try:
        module = importlib.import_module(module_name)
        result = module.handle_request(request)
        return HttpResponse(result)
    except Exception:
        return HttpResponse(f"No handler found for {folder_name}.")


@require_http_methods(["GET"])
def jiekou(request):
    chongzu = []
    listnum = 1

    def is_https():
        if 'HTTPS' in os.environ and os.environ['HTTPS'] == 'on':
            return True
        elif 'HTTP_X_FORWARDED_PROTO' in os.environ and os.environ['HTTP_X_FORWARDED_PROTO'] == 'https':
            return True
        elif request.is_secure():
            return True
        else:
            return False

    data = os.listdir("./api")
    for value in data:
        if value != '.' and value != '..' and os.path.isdir(os.path.join("./api", value)) and os.path.exists(
                f"./api/{value}/ndata.json"):
            json_contents = open(f"./api/{value}/ndata.json", 'r', encoding='utf-8').read()
            data = json.loads(json_contents)
            chongzu.append({
                "id": listnum,
                "name": data["name"],
                "dz": ('https://' if is_https() else 'http://') + request.get_host() + "/" + value,
                "cs": data["cs"],
                "gg": data["gg"],
                "sl": data["sl"],
                "sj": data["sj"],
                "state": data["state"]
            })
            listnum += 1

    return JsonResponse(chongzu, safe=False)
