import hashlib
import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from login import models
from login.models import UserForm, RegisterForm, Bilibili
import logging

logger = logging.getLogger('stu')  # 指定所用logger


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    # 不允许重复登录
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    # 往session字典内写入用户状态和数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/success/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空
    request.session.flush()
    return redirect("/index/")


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def success(request):
    pass
    return render(request, 's/success.html')


def query(request):
    # arry = models.Bilibili.objects.raw('select * from bilibili')  # RawQuerySet
    # alist = []
    # for item in list(arry):
    #     alist.append(
    #         {'rank_tab': item.分区名称, 'rank_num': item.排名, 'title': item.视频标题, 'href': item.href, 'author': item.作者,
    #          'au_href': item.au_href, 'bvid': item.视频id})
    # return alist
    pass
    return render(request, 's/query.html')


def bl_json(request):
    response = {}
    # 分页
    offset = int(request.GET.get('offset'))
    limit = int(request.GET.get('limit'))
    keyword = request.GET.get('KEYW')
    if keyword:
        bl_list = models.Bilibili.objects.values('rank_tab', 'rank_num', 'title', 'href', 'author', 'au_href', 'bvid').filter(
            rank_tab__contains=keyword).order_by("rank_tab")
    else:
        bl_list = models.Bilibili.objects.values('rank_tab', 'rank_num', 'title', 'href', 'author', 'au_href', 'bvid').order_by("rank_tab")
    if bl_list:
        paginator = Paginator(bl_list, limit)
        try:
            page_object_list = paginator.page(offset / limit + 1)
            logger.info('获取数据成功,path：' + request.path)
        except PageNotAnInteger:
            logger.error('If page is not an integer, deliver first page.,path：' + request.path)
            page_object_list = paginator.page(1)
        except EmptyPage:
            logger.error('If page is out of range (e.g. 9999), deliver last page of results.,path：' + request.path)
            page_object_list = paginator.page(paginator.num_pages)

        # rows = []
        # for item in page_object_list:
        #     # 将数组中的每个元素提取出来拼接为rows的内容
        #     rows.append({'rank_tab': item['分区名称'], 'rank_num': item['排名'], 'title': item['视频标题'], 'href': item['href'],
        #                  'author': item['作者'], 'au_href': item['au_href'], 'bvid': item['视频id']})
        response["records"] = page_object_list.object_list
        if keyword:
            response['total'] = models.Bilibili.objects.filter(rank_tab__contains=keyword).count()
        else:
            response['total'] = models.Bilibili.objects.all().count()
    return JsonResponse(response)


def error(request):
    pass
    return render(request, 's/error.html')