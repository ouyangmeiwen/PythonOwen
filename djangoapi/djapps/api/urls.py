from django.urls import path
from .views_list.hello_view import hello
from .views_list.libitem_view import libitem

urlpatterns = [
    path('hello', hello),
    path('libitem', libitem),
]