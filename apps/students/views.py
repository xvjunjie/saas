from django.shortcuts import render
from django.views import View

from users.models import UserInfo


# Create your views here.
class StudentView(View):
    def get(self,request):
        users  = UserInfo.objects.filter(is_admin = '0', is_delete = False).order_by("-create_time").all()
        print(users)

        return render(request, 'login.html')

    def update(self,request):
        pass