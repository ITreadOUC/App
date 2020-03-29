from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
# 内置user的登录注销以及判断登录
# from django.contrib.auth import login as log_in
# from django.contrib.auth import logout as log_out
# from django.contrib.auth.decorators import login_required
# 用于密码加密解密
from django.contrib.auth.hashers import make_password, check_password
# 使用model类
from app.models import User, Books, Short, Long, Type, State
# 用于发送邮件
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
# 用于正则表达式
import re
# 用于生成随机函数
import random

# Create your views here.


# 登录表单提交函数
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            exist_user = User.objects.filter(username=username).first()
            if exist_user:
                exist_password = check_password(password, exist_user.password)
                if exist_password:
                    if exist_user.is_active == 1:
                        request.session['user'] = exist_user.first().username
                        result = '登陆成功'
                    else:
                        result = '该用户已经被冻结'
                else:
                    result = '用户名或者密码错误'
            else:
                result = '用户名不存在'
        else:
            result = '未提交全部参数'
    else:
        result = '未提交POST请求'
    json = {"result": result}
    return JsonResponse(json)


# 随机code生成函数
def get_code():
    code = random.randint(100000, 999999)
    return code


# 发送邮件的函数
def send_mail(email, code):
    # 发件人邮箱账号
    my_sender = '1559492576@qq.com'
    # 发件人邮箱密码
    my_pass = "uybwmelwsltjjbej"
    # 收件人邮箱账号
    my_user = email
    content = '''
    亲爱的用户：
        您好！
        欢迎您加入我们爱特读书大家庭!
        一定保存好验证码,打死也不要告诉别人哦！
    '''
    content = content + "    您的注册验证码为:" + str(code)
    # 括号里包括邮件主要内容、编码方式
    msg = MIMEText(content, 'plain', 'utf-8')
    # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['From'] = formataddr(["【爱特读书APP】", my_sender])
    # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['To'] = formataddr(["爱特读书用户", my_user])
    # 邮件的主题，也可以说是标题
    msg['Subject'] = "【爱特读书验证码发送】"
    # 发件人邮箱中的SMTP服务器，端口是465
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 括号中对应的是发件人邮箱账号、邮箱密码
    server.login(my_sender, my_pass)
    # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    print("邮件发送成功")
    server.quit()


# 判断是否登录-Python装饰器
def login_required(func):
    def wrapper(request, *args, **kwargs):
        username = request.session.get('user')
        user = User.objects.filter(username=username).first()
        if user:
            setattr(request, 'user', user)
            result = func(request, *args, **kwargs)
            return result
        else:
            json = {"result": '用户未登录'}
            return JsonResponse(json)
    return wrapper


# 注册表单提交函数
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        name = request.POST.get('name')
        image = request.FILES.get('image')
        code = get_code()
        if username and email and password and repassword and name and image:
            un = re.findall(r"^[a-z0-9_]{6,16}$", username)
            pd = re.findall(r"^[a-z0-9_.]{6,16}$", password)
            em = re.findall(r"^[a-z0-9]+[@][a-z0-9]+\.com|cn$", email)
            exist_user = User.objects.filter(username=username)
            if exist_user:
                result = '用户名已经存在'
            elif password != repassword:
                result = '两次密码不一致'
            elif not(un and un[0] == username):
                result = '用户名格式不正确'
            elif not(pd and pd[0] == password):
                result = '密码格式不正确'
            elif not(em and em[0] == email):
                result = '邮箱格式不正确'
            elif len(name) > 16:
                result = '昵称格式不正确'
            elif 1 != 1:
                result = '头像格式不正确'
            else:
                u = User()
                u.username = username
                u.password = make_password(password)
                u.email = email
                u.name = name
                u.image = image
                u.code = code
                u.is_active = 0
                u.save()
                send_mail(email, code)
                result = '验证码发送成功'
        else:
            result = '未提交全部参数'
    else:
        result = '未提交POST请求'
    json = {"result": result}
    return JsonResponse(json)


# 验证码验证页
def check_code(request):
    if request.method == "POST":
        username = request.POST.get('username')
        code = request.POST.get('code')
        if username and code:
            exist_user = User.objects.filter(username=username).first()
            if exist_user:
                is_active = exist_user.is_active
                if is_active == 0 and exist_user.code is not None:
                    if int(code) == exist_user.code:
                        User.code = None
                        User.is_active = 1
                        User.save()
                        result = '验证码验证成功'
                    else:
                        result = '验证码错误'
                else:
                    result = '用户名已经激活'
            else:
                result = '用户名不存在'
        else:
            result = '未提交全部参数'
    else:
        result = '未提交POST请求'
    json = {"result": result}
    return JsonResponse(json)


@login_required
def logout(request):
    result = '退出登录成功'
    del request.session['user']
    json = {"result": result}
    return JsonResponse(json)


def forget_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')
        if username and email:
            exist_user = User.objects.filter(username=username).first()
            if exist_user:
                if email == exist_user.email:
                    pd = re.findall(r"^[a-z0-9_.]{6,16}$", new_password)
                    if pd and pd[0] == new_password:
                        if new_password == re_password:
                            if exist_user.is_active == 0:
                                code = get_code()
                                exist_user.code = code
                                exist_user.is_active = 0
                                exist_user.password = make_password(new_password)
                                exist_user.save()
                                send_mail(email, code)
                                result = '验证码发送成功'
                            else:
                                result = '该用户已经被冻结'
                        else:
                            result = '两次密码不一致'
                    else:
                        result = '新密码格式不正确'
                else:
                    result = '用户名与邮箱不匹配'
            else:
                result = '用户名不存在'
        else:
            result = '未提交全部参数'
    else:
        result = '未提交POST请求'
    json = {"result": result}
    return JsonResponse(json)


@login_required
def change_password(request):
    user = User.objects.filter(username=request.user).first()
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')
        if old_password and new_password and re_password:
            exist_password = check_password(old_password, user.password)
            if exist_password:
                if new_password == re_password:
                    pd = re.findall(r"^[a-z0-9_.]{6,16}$", new_password)
                    if pd and pd[0] == new_password:
                        user.password = make_password(new_password)
                        user.save()
                        result = '密码修改成功'
                    else:
                        result = '新密码格式不正确'
                else:
                    result = '两次密码不一致'
            else:
                result = '原密码不正确'
        else:
            result = '未提交全部参数'
    else:
        result = '未提交POST请求'
    json = {"result": result}
    return JsonResponse(json)


@login_required
def change_name(request):
    user = User.objects.filter(username=request.user).first()
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            if len(name) <= 16:
                user.name = name
                user.save()
                result = '昵称修改成功'
            else:
                result = '昵称格式不正确'
        else:
            result = '未提交全部参数'
    else:
        result = '未提交POST请求'
    json = {"result": result}
    return JsonResponse(json)


@login_required
def change_image(request):
    user = User.objects.filter(username=request.user).first()
    image = request.FILES.get('image')
    if image:
        if 1 == 1:
            user.image = image
            user.save()
            result = '头像修改成功'
        else:
            result = '图片格式不正确'
    else:
        result = '未上传图片'
    json = {"result": result}
    return JsonResponse(json)


@login_required
def index(request):
    user = User.objects.filter(username=request.user).first()
    user_index = {
        "username": user.username,
        "nickname": user.name,
        "icon": user.image,
        "email": user.email,
    }
    want_read = []
    reading = []
    have_read = []
    books = user.state_set.all()
    for book in books:
        if book.state == 0:
            book_index = Books.objects.filter(id=book.book).first()
            temp = {
                "bookname": book_index.image,
                "bookphoto": book_index.title,
                "author": book_index.author,
                "publish": book_index.publish,
                "publish_time": book_index.publish_time,
                "isbn": book_index.isbn,
                "book_num": book_index.id,
            }
            want_read.append(temp)
        elif book.state == 1:
            book_index = Books.objects.filter(id=book.book).first()
            temp = {
                "bookname": book_index.image,
                "bookphoto": book_index.title,
                "author": book_index.author,
                "publish": book_index.publish,
                "publish_time": book_index.publish_time,
                "isbn": book_index.isbn,
                "book_num": book_index.id,
            }
            reading.append(temp)
        else:
            book_index = Books.objects.filter(id=book.book).first()
            temp = {
                "bookname": book_index.image,
                "bookphoto": book_index.title,
                "author": book_index.author,
                "publish": book_index.publish,
                "publish_time": book_index.publish_time,
                "isbn": book_index.isbn,
                "book_num": book_index.id,
            }
            have_read.append(temp)
    json = {
        "user": user_index,
        "want_read": want_read,
        "reading": reading,
        "have_read": have_read,
        "result": '用户已登录',
    }
    return JsonResponse(json)







