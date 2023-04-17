import uuid

from django.contrib.auth import authenticate, login
from django.db.models import Max, Avg, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from users.models import UserInfo, Course, Record


# Create your views here.


# 主界面
def index(request):
    context = {
        'status': '未登录状态'
    }
    return render(request, 'users/index.html', context)


# 增加数据 增加只能root用户或者管理员才能操作
def add(request):
    if request.method == "POST":
        login_user = request.session['user']
        id = login_user['id']
        is_admin = UserInfo.objects.get(id=id).is_admin
        if is_admin == "1":
            stu_id = request.POST.get('stu_id', uuid.uuid1())
            stu_name = request.POST.get('stu_name')
            grade = request.POST.get('grade')
            course = request.POST.get('course')

            if not all([stu_id, stu_name]):
                context = {
                    'msg': '学号和名字有遗漏',
                }
                return render(request, 'users/add.html', context)

            stu_data = UserInfo()
            stu_data.stu_id = stu_id
            stu_data.username = stu_name
            stu_data.stu_name = '123456'
            stu_data.save()
            context = {
                'sucess': '增加成功',
            }
            return render(request, 'users/add.html', context)
        else:
            context = {
                'error': '只用root用户和管理员才能操作'
            }
            return render(request, 'users/add.html', context)
    else:

        # course = Course.objects.all()
        # context = {"course":course}
        return render(request, 'users/add.html')


# 查询
def select(request):
    if request.method == "POST":
        id = request.POST.get('stu_id')
        stu_data = UserInfo.objects.get(user_no=id)
        stu_id = stu_data.user_no
        stu_name = stu_data.username
        stu_record = Record.objects.filter(user_no=id)
        avg ,total = stu_record.aggregate(Avg('grade'),Sum('grade'))

        context = {
            'stu_id': stu_id,
            'stu_name': stu_name,
            'course_data': stu_record,
            'total': total.get("grade__sum"),
            'avg': avg.get("grade__avg"),
            'msg': True
        }
        return render(request, 'users/select.html', context)
    else:
        root_information = request.session['user']
        id = root_information['user_id']
        context = {
            'msg': False,
            'id': id
        }
        return render(request, 'users/select.html', context)


class UsersView(View):
    '''
        get:
            获取全部人员
        post:、
            添加
        update:
            修改
        delete：
            删除

    '''


    def get(self, request):
        users = UserInfo.objects.filter(is_delete=False).order_by("-create_time").all()
        print(users)
        context = {
            "users":users
        }

        return render(request, 'studentManage/add.html')

    def post(self,request):
        user_no = request.POST.get('user_no')
        username = request.POST.get('username')
        if not all([user_no, username]):
            context = {
                'msg': '学号和名字有遗漏',
            }
            return render(request, 'studentManage/add.html', context)


        login_user = request.session['user']
        user_id = login_user.get('user_id')
        user = UserInfo.objects.filter(id=user_id)
        if user:
            if user.is_admin == "1": #管理员
                UserInfo.creat(user_no=user_no,username = username)
                context = {}
                return render(request, 'studentManage/add.html', context)
            else:
                context = {
                    'error': '只用root用户和管理员才能操作'
                }
                return render(request, 'studentManage/add.html', context)






    def update(self, request):
        pass





class RegisterView(View):
    def get(self,request):
        return render(request, 'users/register.html')

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username and password:
            user = UserInfo.objects.filter(username=username)
            if user:

                context= {

                }
                return render(request, 'register.html', {
                    'msg': '用户已存在'
                })
            else:
                user = UserInfo()
                user.username = username
                user.password = password
                user.user_no = uuid.uuid1()
                user.set_password(password)
                user.save()
                return render(request, 'users/login.html')
        else:
            context = {

            }
            return  HttpResponse(context)


class LoginView(View):
    def get(self,request):
        return render(request, 'users/login.html')

    def post(self,request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        is_admin = request.POST.get('is_admin', 1)

        if all([username , password , is_admin]):
            user = authenticate(username=username, password=password, is_admin=is_admin)
            if user:
                login(request, user)
                request.session['user'] = {
                    'user_id': user.id,
                    'username': user.username,
                    'user_no': user.user_no,
                    'is_admin': user.is_admin,
                }
                return render(request, 'users/index.html')

            else:
                return render(request, 'login.html', {
                    'msg': '用户名或密码错误'
                })
        else:
            return render(request, 'login.html', {
                'msg': '参数不能为空'
            })