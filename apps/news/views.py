from django.shortcuts import render
from django.views.decorators.http import require_POST
from apps.cms.models import News
from .serializers import NewsListSerializer, CommentSerializer, WebCommentSerializer
from django.conf import settings
from utils import restful
from .models import Comment, WebComment
from django.http import HttpResponse
from django.template.defaultfilters import escape
from .forms import CommentForm, WebDiscussForm


def index_view(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category', 'author').all()[0:count]
    web_comments = WebComment.objects.select_related('author').all()
    context = {
        'newses': newses,
        'web_comments': web_comments
    }
    return render(request, 'index/index.html', context=context)


def personal_space_view(request):
    newses = News.objects.select_related('author', 'category').filter(category__name='个人博客')
    context = {
        'newses': newses
    }
    return render(request, 'basketball/basketball.html', context=context)


def news_list_view(request):
    page = int(request.GET.get('p', 1))
    start = int((page - 1) * settings.ONE_PAGE_NEWS_COUNT)
    end = int(start + settings.ONE_PAGE_NEWS_COUNT)
    newses = News.objects.select_related('category', 'author').all()[start:end]
    serializer = NewsListSerializer(newses, many=True)
    return restful.result(data=serializer.data)


def news_detail_view(request, news_id):
    try:
        # news = News.objects.select_related('author', 'category').get(pk=news_id)
        # comments = Comment.objects.select_related('comment_author').filter(comment_news=news_id)
        # 对上面代码进行优化，使用select_related可以对当前查询的model下的外键字段进行关联查询，数据库中使用的是join方法。prefetch_related另外一个模型的字段是当前模型的外键，进行反向查询。selected_related只能放在prefetch_related前面，否则无效。适用多对多
        news = News.objects.select_related('author', 'category').prefetch_related('comments__comment_author', ).get(
            pk=news_id)

        return render(request, 'news/news_detail.html', context={
            'news': news,
            # 'comments': comments
        })
    except News.DoesNotExist:
        return HttpResponse('访问的文章不存在！请正确浏览网页。。。')


@require_POST
def news_comment_view(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        try:
            content = escape(form.cleaned_data.get('comment_content'))  # 对提取出来的数据进行转义，即使django模板默认转义。
            news_id = form.cleaned_data.get('news_id')
            news = News.objects.get(pk=news_id)  # 这里必须将新闻查询到，不能直接将id保存到数据库中，会报错。当保存时数据中要保存实列，而不是一个id
            comment = Comment.objects.create(comment_content=content, comment_news=news,
                                             comment_author=request.user)  # 评论的作者直接从request中获取
            serializer = CommentSerializer(comment)
            return restful.result(data=serializer.data)
        except News.DoesNotExist:
            return HttpResponse(status_code=404)
    else:
        return restful.params_error(message=form.get_errors())


@require_POST
def comment_view(request):
    form = WebDiscussForm(request.POST)
    if form.is_valid():
        comment = escape(form.cleaned_data.get('comment'))
        web_comment = WebComment.objects.create(comment=comment, author=request.user)
        serializer = WebCommentSerializer(web_comment)
        return restful.result(data=serializer.data)
    else:
        return restful.params_error(message=form.get_errors())
