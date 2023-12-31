# Generated by Django 4.2.3 on 2023-07-17 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='分类')),
                ('seq', models.IntegerField(default=1, verbose_name='排序')),
            ],
        ),
        migrations.CreateModel(
            name='FileRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_name', models.CharField(max_length=200, verbose_name='源文件名称')),
                ('file_name', models.CharField(max_length=200, verbose_name='文件名称')),
                ('file_path', models.FilePathField(max_length=255, verbose_name='文件路径')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('suffix', models.CharField(max_length=10, verbose_name='文件类型')),
                ('file_net_path', models.CharField(max_length=200, verbose_name='文件网络路径')),
            ],
        ),
        migrations.CreateModel(
            name='NUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20, verbose_name='手机号')),
                ('identity_number', models.CharField(max_length=50, verbose_name='身份证号')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('invitation_code', models.CharField(max_length=20, verbose_name='邀请码')),
                ('real_name', models.CharField(max_length=10, verbose_name='手机号')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('approval_status', models.SmallIntegerField(choices=[(1, 'PASS'), (0, 'NO_APPROVAL'), (-1, 'REJECT')], default=0, verbose_name='审核状态')),
                ('approval_time', models.DateTimeField(auto_now_add=True, verbose_name='审核时间')),
                ('reject_reason', models.TextField(verbose_name='拒绝原因')),
                ('max_invitation_number', models.IntegerField(default=10, verbose_name='最大邀请')),
                ('identity_photo', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='identity_photo', to='blog.filerecord', verbose_name='身份证照片')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='标签')),
            ],
        ),
        migrations.CreateModel(
            name='NUserRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitation_user', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='invitation_user', to='blog.nuser', verbose_name='用户')),
                ('invited_user', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='invited_user', to='blog.nuser', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='标题')),
                ('intro', models.TextField(blank=True, max_length=200, verbose_name='摘要')),
                ('html_text', models.TextField(blank=True)),
                ('markdown_text', models.TextField(blank=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('type', models.SmallIntegerField(choices=[(1, 'ARTICLE'), (2, 'NEWS'), (3, 'MEDIA')], default=1, verbose_name='类型')),
                ('status', models.SmallIntegerField(choices=[(1, 'RELEASE'), (0, 'PADDING'), (-1, 'DELETE')], default=1, verbose_name='状态')),
                ('is_top', models.BooleanField(default=True, verbose_name='是否在首页显示')),
                ('category', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='分类')),
                ('cover', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cover', to='blog.filerecord', verbose_name='封面')),
                ('music', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='music', to='blog.filerecord', verbose_name='音乐路径')),
                ('tags', models.ManyToManyField(blank=True, to='blog.tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
        ),
    ]
