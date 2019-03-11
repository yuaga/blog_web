from datetime import datetime

from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.views import View
from django.views.decorators.http import require_POST

from apps.login.models import User
from .models import NewsCategory, News
from .forms import WriteNewsForm, EditNewsForm
from utils import restful
from django.conf import settings
import os
from django.core.paginator import Paginator


# cms管理主页
def cms_index(request):
    return render(request, 'cms/index.html')


# cms新闻分类页面
def cms_news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/category.html', context=context)


# 新增新闻分类
def cms_add_category(request):
    name = request.POST.get('name')
    if not NewsCategory.objects.filter(name=name).exists():
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='分类已存在')


# 编辑新闻分类，在这里要对输入的分类进行form验证
# 经验证，使用form表单进行数据验证时，当进行分类是否存在时，不会弹出错误信息
# def cms_edit_category(request):
#     form = EditCategoryForm(request.POST)
#     if form.is_valid():
#         pk = form.cleaned_data.get('id')
#         new_name = form.cleaned_data.get('name')
#         try:
#             NewsCategory.objects.filter(pk=pk).update(name=new_name)
#             return restful.ok()
#         except:
#             return restful.params_error(message='分类已存在！')
#     else:
#         return restful.params_error(message=form.get_errors())


# 编辑新闻
def cms_edit_category(request):
    pk = request.POST.get('pk')
    new_name = request.POST.get('name')
    if len(new_name) < 6:
        if not NewsCategory.objects.filter(name=new_name).exists():
            NewsCategory.objects.filter(pk=pk).update(name=new_name)
            return restful.ok()
        else:
            return restful.params_error(message='分类已存在')
    else:
        return restful.params_error(message='输入的分类超过了6个字符，请重新编辑！')


# 删除新闻分类
def cms_del_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.get(pk=pk).delete()
        return restful.ok()
    except NewsCategory.DoesNotExist:
        return HttpResponse(status=404)


# cms发布新闻页面
class CmsWriteNews(View):
    def get(self, request):
        return render(request, 'cms/write_news.html', context={
            'categories': NewsCategory.objects.all()
        })

    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            News.objects.create(title=title, category=category, desc=desc, thumbnail=thumbnail, content=content,
                                author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


# cms编辑新闻
class CmsNewsEdit(View):

    def get(self, request):
        pk = request.GET.get('news_id')
        return render(request, 'cms/write_news.html', context={
                            'news': News.objects.get(pk=pk),
                            'categories': NewsCategory.objects.all(),
                        })

    def post(self, request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('id')
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            News.objects.filter(pk=pk).update(title=title, category=category, desc=desc, thumbnail=thumbnail,
                                              content=content)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


# cms新闻删除
@require_POST
def cms_del_news_view(request):
    try:
        pk = request.POST.get('pk')
        News.objects.get(pk=pk).delete()
        return restful.ok()
    except News.DoesNotExist:
        return restful.params_error(message='要删除的新闻不存在！')


# cms新闻管理页面
class CmsNewsManage(View):

    def get(self, request):
        page = int(request.GET.get('p', 1))  # 获取当前的页码, 如果没有拿到，默认第一页，保险起见，转化为整数。
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category') or 0)  # 获取分类的id, 如果没有就默认为1

        # 使用select_related提前将相关联的数据提取出来，避免模板中在一次查询
        newses = News.objects.select_related('category', 'author')

        if start or end:
            if start:
                # 将字符串时间改为格式化的时间
                start = datetime.strptime(start, '%Y/%m/%d')
            else:
                # 如果没有设置开始查询时间，则默认使用2019/01/01
                start = datetime(year=2019, month=1, day=1)
            if end:
                end = datetime.strptime(end, '%Y/%m/%d')
            else:
                end = datetime.today()

            newses = newses.filter(pub_time__range=(make_aware(start), make_aware(end)))
            # newses = newses.filter(pub_time__range=(start, end))

        if title:
            newses = newses.filter(title__icontains=title)

        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 2)   # 要实现分页的模型的对象是newses， 每页2条数据。
        page_obj = paginator.page(page)  # 获取当前页的对象

        context = {
            # object_list 方法是将当前页的所有对象放入列表中，方便前端遍历
            'page_objs': page_obj.object_list,  # 这个地方不能再传newses了，因为要显示分页后的数据
            'categories': NewsCategory.objects.all(),
            'title': title,
            'category_id': category_id,
            'paginator': paginator,
            'current_page': page_obj.number,
            'num_pages': paginator.num_pages,
            'page_obj': page_obj,  # 后面4项一定要传，如果没有传，在模板中调用这三个方法是不行的。
        }
        return render(request, 'cms/news_manage.html', context=context)


# 上传图片到自己的服务器
@require_POST
def upload_file_view(request):
    # 从ajax中提取传过来的文件,get中的字段与js代码中append内的要保持一致
    # js代码中已经将文件存放到formData中，并传了过来
    file = request.FILES.get('file')
    # 获取file的名字
    name = file.name
    # 将xx名字的文件打开以二进制写入的方式,从file的chunks()中获取并写入到fp中
    # 使用with的好处就是简洁强大，一般方法繁琐且容易忘记关闭文件。
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    # 上传文件需要得到文件的url
    # request的build_absolute_uri方法是获取一个绝对url http://127.0.0.1:8000
    # 最后的url就算http://127.0.0.1:8000/media/abc.png
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.result(data={'url': url})


# cms员工管理页面
def cms_staff_manage(request):
    staffs = User.objects.filter(is_staff=True)
    groups = Group.objects.all()
    context = {
        'staffs': staffs,
        'groups': groups
    }
    return render(request, 'cms/staffs.html', context=context)
