from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class MyPagination(PageNumberPagination):
    # 每页返回条数
    page_size = 10

    # 指定查询字符串的key值(?/key=条数),不重写的话默认key值为'page'
    page_query_param = 'page'

    # 指定前端返回的每页条数的key值,不指定的话前端无法开启每页返回条数指定功能(?/s=条数)
    page_size_query_param = 'size'

    # 每页最多显示条数
    max_page_size = 50

    def get_paginated_response(self, data):
        # 调用父类的get_paginated_response获取页数相关信息
        response = super().get_paginated_response(data)
        # 当前所在的页数
        response.data['current_page_num'] = self.page.number
        # 总计最大页数
        response.data['total_pages'] = self.page.paginator.num_pages
        # 只在接口文档中生效
        page_query_description = '第几页'
        page_size_query_description = '每页几条'

        return response

        # # 重写父类方法,但是需要导入部分模块,较为繁琐不太推荐
        # current_page_num = self.page.number
        # total_pages = self.page.paginator.num_pages

        # return Response(OrderedDict([
        #     ('count', self.page.paginator.count),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data),
        #     ('current_page_num', current_page_num),
        #     ('total_pages', total_pages)
        # ]))
