from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import *
from rest_framework.views import APIView
from ..model_list.libitem import Libitem
from ..utils_lst.string_helper import convert_model_to_dict
from rest_framework.permissions import AllowAny

class LibItemView(APIView):
    authentication_classes = [JWTAuthentication]  # 使用 JWT 认证
    #permission_classes = [IsAuthenticated]       # 需要认证才能访问
    permission_classes = [AllowAny]       # 需要认证才能访问
    # curl http://127.0.0.1:9001/api/libitem?name=Owen
    # http://127.0.0.1:9001/api/libitem?page=1&size=10
    def get(self, request):
        libitemallquery = Libitem.objects.all().order_by('-creationtime', 'barcode')

        # 获取分页参数
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('size', 10)

        paginator = Paginator(libitemallquery, page_size)
        total_count = paginator.count 

        try:
            page_objs = paginator.page(page_number)
        except:
            return JsonResponse({'msg': 'Page not found'}, status=404)

        # 转换数据库对象
        datas = [convert_model_to_dict(item) for item in page_objs]

        # 构建返回的 JSON 结果
        response_data = {
            'total_count': total_count,  # 总记录数
            'page_number': int(page_number),  # 当前页码
            'page_size': int(page_size),  # 每页大小
            'datas': datas  # 数据内容
        }
        return JsonResponse(response_data)
