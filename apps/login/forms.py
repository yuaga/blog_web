from django import forms
from apps.forms import FormMixin


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11, label='手机号码',
                                error_messages={'max_length': '请正确输入手机号码！', 'min_length': '请输入11位手机号码！'})
    password = forms.CharField(max_length=16, min_length=8, label='密码',
                               error_messages={'max_length': '密码输入错误！', 'min_length': '密码输入错误！', })
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11, label='手机号码',
                                error_messages={'max_length': '请正确输入手机号码！', 'min_length': '请输入11位手机号码！'})
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=16, min_length=8, label='密码',
                                error_messages={'max_length': '密码长度太长！', 'min_length': '密码不足8位！'})
    password2 = forms.CharField(max_length=16, min_length=8, label='确认密码',
                                error_messages={'max_length': '密码长度太长！', 'min_length': '密码不足8位！'})
    img_captcha = forms.CharField(max_length=4, min_length=4,
                                  error_messages={'max_length': '请正确填写验证码！', 'min_length': '请正确填写验证码！'})
