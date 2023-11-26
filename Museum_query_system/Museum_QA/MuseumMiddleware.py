#自定义中间件类，做登录判断处理
from django.shortcuts import redirect
from django.urls import  reverse
import re

class MuseumMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("MuseumMiddleware")
        # One-time configuration and initialization.

    def __call__(self, request):
        path=request.path
        print("url:",path)#获取当前请求的url
        # 权限限制，如果没有登录，重定向到admin界面

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        #判断是否登录

        # 定义后台不登录也允许访问的url列表
        urllist=['/Museum_QA/admin/','/Museum_QA/','/Museum_QA/query/']
        #判断当前请求url地址以什么开头 后台/manage,并且不在urlist中才做是否登录判断
        if path not in urllist:
            if 'username' not in request.session:
                return redirect('../admin/')#反向解析登录页面url地址
            #重定向到登录页

        #放行的意思，直接响应
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response