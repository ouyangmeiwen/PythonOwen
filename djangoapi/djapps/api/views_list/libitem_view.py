from django.http import *
import json
from django.core.paginator import Paginator

from ..model_list.libitem import (Libitem)
from ..utils_lst.string_helper import *
# curl http://127.0.0.1:9001/api/libitem?name=Owen
# http://127.0.0.1:9001/api/libitem?name=Owen
def libitem(request):
    libitemallquery=Libitem.objects.all()
    libitemallquery=libitemallquery.order_by('-creationtime','barcode')
    page_number = 1
    page_size = 10
    # 创建分页器
    paginator = Paginator(libitemallquery, page_size)
    total_count = paginator.count 
    # 获取当前页的数据
    try:
        page_objs = paginator.page(page_number)
    except:
        return JsonResponse({'msg': 'Page not found'})

    #转换获得的结果
    libitems=list(page_objs)
    #构建返回的结果
    datas=[]
    #循环递归处理
    for item in libitems:
        #转换数据库对象
        data=convert_model_to_dict(item)
        datas.append(data)
     # 返回JSON格式的响应
    response_data = {
        'total_count': total_count,  # 返回总记录数
        'page_number': page_number,  # 返回当前页
        'page_size': page_size,      # 返回每页数据量
        'datas': datas               # 返回数据内容
    }
    return JsonResponse(response_data)  # 404 Not Found