from django.http import *
import json
from django.core.paginator import Paginator

from ..model_list.libitem import (Libitem)
from ..utils_lst.string_helper import *

# curl http://127.0.0.1:9001/api/hello?name=Owen
# http://127.0.0.1:9001/api/hello?name=Owen
def hello(request):
    user_agent = request.headers.get('User-Agent', 'Unknown')
    print("user_agent:"+user_agent)
    params = {}
    if request.method == 'GET':
        params = request.GET.dict()  # 获取 GET 参数
        print("GET:", params)  # 直接打印字典，避免字符串拼接错误
    elif request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                params = json.loads(request.body)  # 解析 JSON
                print("POST:",(params))
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            params = request.POST.dict()  # 获取表单数据
            print("Form:",(params))
    return JsonResponse({'params': params})