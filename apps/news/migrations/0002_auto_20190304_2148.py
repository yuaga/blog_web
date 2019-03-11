# Generated by Django 2.1.7 on 2019-03-04 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(max_length=150)),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='News',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cms.News'),
        ),
        migrations.AddField(
            model_name='comment',
            name='origin_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.Comment'),
        ),
    ]
