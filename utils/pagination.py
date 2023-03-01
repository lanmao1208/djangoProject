from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    # 每页返回条数
    page_size = 4

    # 指定查询字符串的key值(?/key=条数),不重写的话默认key值为'page'
    page_query_param = 'p'

    # 指定前端返回的每页条数的key值,不指定的话前端无法开启每页返回条数指定功能(?/s=条数)
    page_size_query_param = 's'

    # 每页最多显示条数
    max_page_size = 50