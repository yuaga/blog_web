from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.core import validators


class UserManager(BaseUserManager):

    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError('请输入手机号码！')
        if not username:
            raise ValueError('请输入用户名！')
        if not password:
            raise ValueError('请输入密码！')
        # self.model 表示User
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)  # 设置密码，这样的密码才会进行加密
        user.save()
        return user

    # 创建普通用户
    def create_user(self, telephone, username, password, **kwargs):
        return self._create_user(telephone=telephone, username=username, password=password, **kwargs)

    # 创建超级用户
    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self._create_user(telephone=telephone, username=username, password=password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # django自带的User模型很强大，但是有些字段在这个项目中不需要，所以重写User模型。
    uuid = ShortUUIDField(primary_key=True)  # 采用uuid作为主键，而不是使用数据库中那种数字主键，这样别人就无法知道具体有多少用户
    telephone = models.CharField(max_length=11, unique=True, validators=[validators.RegexValidator(r'1[35678]\d{9}')])
    username = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)  # 是否可用，用来拉黑用户
    is_staff = models.BooleanField(default=False)  # 是否为员工
    is_superuser = models.BooleanField(default=False)  # 是否为超级用户
    date_joined = models.DateTimeField(auto_now_add=True)  # 加入的时间

    USERNAME_FIELD = 'telephone'  # 作为唯一认证标识，当需要对用户进行验证时，将telephone作为认证字段，原来user模型默认的为username
    REQUIRED_FIELDS = ['username']  # 创建超级用户时，用来提醒的字段，设置后会提示填写 telephone username password

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
