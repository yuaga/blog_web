from django.db import models


class Comment(models.Model):
    comment_content = models.TextField(max_length=150)
    pub_time = models.DateTimeField(auto_now_add=True)
    comment_author = models.ForeignKey('login.User', on_delete=models.CASCADE)
    comment_news = models.ForeignKey('cms.News', on_delete=models.CASCADE, related_name='comments')
    origin_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)  # 2级评论，可以为空

    class Meta:
        ordering = ['-pub_time']


class WebComment(models.Model):
    comment = models.TextField(max_length=50)
    pub_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('login.User', on_delete=models.CASCADE)
