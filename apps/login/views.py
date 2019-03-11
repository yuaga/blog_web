from io import BytesIO
from utils.captcha.imgcapacha import Captcha
from django.shortcuts import render, reverse, redirect
from django.core.cache import cache
from django.http import HttpResponse
from django.views import View
from .forms import LoginForm, RegisterForm
from .models import User
from django.contrib.auth import authenticate, login, logout


class LoginView(View):

    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            # 从form表单中拿到数据后，需要进行验证
            user = authenticate(request, username=telephone, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                        return redirect(reverse('index'))
                else:
                    context = {
                        'message': '你的账号已经飞往银河系！'
                    }
                    return render(request, 'login/login.html', context=context)
            else:
                if User.objects.filter(telephone=telephone).exists():
                    context = {
                        'message': '密码错误，请仔细想想！'
                    }
                    return render(request, 'login/login.html', context=context)
                else:
                    context= {
                        'message': '手机号码不存在，请注册！'
                    }
                    return render(request, 'register/register.html', context=context)
        else:
            context = {
                'message': form.get_errors()
            }
            return render(request, 'login/login.html', context=context)


class RegisterView(View):

    def get(self, request):
        return render(request, 'register/register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            img_captcha = form.cleaned_data.get('img_captcha')
            cache_img_captcha = cache.get(img_captcha.lower())
            exists = User.objects.filter(telephone=telephone).exists()
            if not exists:
                if password2 == password1:
                    if cache_img_captcha == img_captcha.lower():
                        user = User.objects.create_user(telephone=telephone, username=username, password=password1)
                        login(request, user)
                        return redirect(reverse('index'))
                    else:
                        context = {
                            'message': '验证码输入错误！'
                        }
                        return render(request, 'register/register.html', context=context)
                else:
                    context = {
                        'message': '两次输入密码不一致，请重新输入！'
                    }
                    return render(request, 'register/register.html', context=context)
            else:
                context = {
                    'message': '你的手机号码已被注册了！'
                }
                return render(request, 'register/register.html', context=context)
        else:
            context = {
                'message': form.get_errors()
            }
            return render(request, 'register/register.html', context=context)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def img_captcha_view(request):
    text, image = Captcha.gene_code()
    # image 不能直接放在response中返回，需要借助流
    out = BytesIO()
    image.save(out, 'png')  # 将image保存入out中，以png这个类型
    out.seek(0)  # 当文件写入后，指针会指向最后，将指针移到最前面

    # HttpResponse 默认存储格式位字符串，此处定义为png格式
    response = HttpResponse(content_type='iamge/png')
    # 再将图片从out中读取出来，保存到response上，read()方法会在指针指向的位置开始读
    response.write(out.read())
    # tell方法可以获取当前指针的位置，代表当前图片的大小
    response['Content-length'] = out.tell()
    #  以字典键值对的方式放入cache  text.lower(): text.lower() ,有效期 5*60秒
    cache.set(text.lower(), text.lower(), 5 * 60)
    return response
