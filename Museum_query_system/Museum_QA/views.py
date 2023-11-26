from django.shortcuts import render
from django.http import HttpResponse
import sys

from django.views.decorators.csrf import csrf_exempt

from Museum_QA.code import main
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import render, HttpResponse, redirect
from Museum_QA.code import dict1
import json


# print(main.get_img("夏莲居和哪个展品有关"))

# 返回多个图片
@csrf_exempt
def get_detail(request):
    context = {}
    # str=""
    if request.POST:
        # if request.GET:
        #     question = request.GET['ask']
        question = request.POST['ask']
        # answer=main.query_function(question)
        # for i in range(0,len(answer)):
        #     str+=answer[i]+" "
        context['rlt'] = main.query_function(question)
        context['pic'] = main.get_img(question)
        context['museum'] = main.get_museum_img(question)
        # pic=main.get_img(question)
        # html = "<span>It is now %s.</span>"

        return HttpResponse(json.dumps(context))
    return render(request, 'query.html')


# 首页
def index(request):
    return render(request, "index.html")


# 增删改查界面
# def admin_add(request):
#     # return render(request,"test.html")
# 管理员登录页面
def admin(request):
    if request.method == 'POST':
        user = request.POST.get('name')
        pwd = request.POST.get('password')
        # 校验
        if user == 'Cathy' and pwd == '123':
            request.session['username'] = user
            request.session['is_login'] = True
            # url重定向
            # request.session['username'] = username
            return redirect("../manage/")
        elif user == 'Jessie' and pwd == 'vivo50':
            request.session['username'] = user
            request.session['is_login'] = True
            return redirect("../manage/")
        elif user == 'Odella' and pwd == 'v587':
            request.session['is_login'] = True
            request.session['username'] = user
            return redirect("../manage/")
    return render(request, 'login.html')


def admin_logout(request):
    del request.session['username']
    request.session.flush()
    return redirect("../admin/")


# 增删改查
def manage(request):
    result = dict1.searchall()
    if request.POST:
        if 'search' in request.POST:
            value = request.POST['search']
            result = dict1.findsearch(value)
        if 'searchall' in request.POST:
            result = dict1.searchall()
        if 'Addone' in request.POST:
            kind = request.POST.get("labels")
            value = request.POST['Addone']
            result = dict1.addonenode(kind, value)
        if "Addrel" in request.POST:
            kind1 = request.POST.get("labels1")
            kind2 = request.POST.get("labels2")
            value = request.POST['Addrel']
            result = dict1.Addrelationship(kind1, value, kind2)
        if 'deletenode' in request.POST:
            # kind2=request.POST.get("labels2")
            value = request.POST['deletenode']
            dict1.deletenode(value)
            result = dict1.query_graph("MATCH (n)-[rel]->(m)  RETURN rel")
        if 'deleteall' in request.POST:
            # kind2=request.POST.get("labels2")
            value = request.POST['deleteall']
            dict1.deleteall()
            result = dict1.query_graph("MATCH (n)-[rel]->(m)  RETURN rel")
    return render(request, 'manage.html', {'data': json.dumps(result['data']), 'link': json.dumps(result['links'])})

# return HttpResponse("Hello, world. You're at the query index.")
# Create your views here.
