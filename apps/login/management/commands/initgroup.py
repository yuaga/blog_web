from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, ContentType
from apps.news.models import WebComment,Comment
from apps.cms.models import News,NewsCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 编辑猿
        # 先通过模型找到对应的content_type
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
        ]
        # 再通过content_type找到对应的权限
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        # 创建分组
        edit_group = Group.objects.create(name='编辑猿')
        # 将权限添加到分组中
        edit_group.permissions.set(edit_permissions)
        edit_group.save()
        self.stdout.write(self.style.SUCCESS('编辑创建好了'))
        # 管理猿
        manage_content_types = [
            ContentType.objects.get_for_model(WebComment),
            ContentType.objects.get_for_model(Comment),
        ]
        manage_permissions = Permission.objects.filter(content_type__in=manage_content_types)
        manage_group = Group.objects.create(name='管理猿')
        manage_group.permissions.set(manage_permissions)
        manage_group.save()
        self.stdout.write(self.style.SUCCESS('管理创建好了'))
