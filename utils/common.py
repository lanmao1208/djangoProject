# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/8/1 10:49 
  @Auth : 可优
  @File : common.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import locale


def datetime_fmt():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    return '%Y年%m月%d日 %H:%M:%S'
