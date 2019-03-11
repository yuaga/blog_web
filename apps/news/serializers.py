from rest_framework import serializers
from apps.cms.models import News, NewsCategory
from apps.login.serializers import UserSerializers
from .models import Comment, WebComment


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'name')


class NewsListSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializers()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'category', 'author', 'pub_time')


class CommentSerializer(serializers.ModelSerializer):
    comment_author = UserSerializers()

    class Meta:
        model = Comment
        fields = ('id', 'pub_time', 'comment_content', 'comment_author', 'origin_comment')


class WebCommentSerializer(serializers.ModelSerializer):
    author = UserSerializers()

    class Meta:
        model = WebComment
        fields = ('pub_time', 'comment', 'author')