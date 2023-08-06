# _*_coding:utf-8_*_
from django.urls import re_path

from .apis.invoice_apis import InvoiceApi

urlpatterns = [
    re_path(r'^add/?$', InvoiceApi.add, ),  # 发票添加
    re_path(r'^edit/?$', InvoiceApi.edit, ),  # 编辑
    re_path(r'^list/?$', InvoiceApi.list, ),  # 列表
    re_path(r'^examine_approve/?$', InvoiceApi.examine_approve, ),  # 列表
]
