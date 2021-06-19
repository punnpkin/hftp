import os
import string
from django.http import response
from django.shortcuts import render


def get_disklist():
    disk_list = []
    for c in string.ascii_uppercase:
        disk = c+':'
        if os.path.isdir(disk):
            disk_list.append(disk)

    return disk_list


def handle_dir(path):
    item_list = os.listdir(path=path+"/")
    dir_list = []
    file_list = []

    for item in item_list:
        if os.path.isdir(path+"/"+item):
            dir_list.append(item)
        else:
            file_list.append(item)

    dir_list = [".."]+dir_list

    return dir_list, file_list


def index(request):
    item_list = get_disklist()
    context = {'item_list': item_list}
    return render(request, "handle/index.html", context)


def update(request):
    if(request.method == 'GET'):
        path = request.GET.get("path")
    
    if path=="":
        item_list = get_disklist()
        context = {'dir_list': item_list, 'file_list':""}
        return response.JsonResponse(context, safe=False)

    elif os.path.isdir(path):
        dir_list, file_list = handle_dir(path)
        context = {'dir_list': dir_list,'file_list':file_list}
        return response.JsonResponse(context, safe=False)

    elif path.split(".")[-1] == "html":
        try:
            res = response.FileResponse(open(path, 'rb'))
            res['content_type'] = "application/octet-stream"
            res['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
            return res
        except Exception:
            raise response.HTTP404

    else:
        return response.HttpResponse("TODO...")
