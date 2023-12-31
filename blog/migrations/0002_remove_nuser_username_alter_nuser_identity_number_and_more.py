# Generated by Django 4.2.3 on 2023-07-17 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='nuser',
            name='identity_number',
            field=models.CharField(blank=True, max_length=50, verbose_name='身份证号'),
        ),
        migrations.AlterField(
            model_name='nuser',
            name='invitation_code',
            field=models.CharField(blank=True, max_length=20, verbose_name='邀请码'),
        ),
        migrations.AlterField(
            model_name='nuser',
            name='real_name',
            field=models.CharField(blank=True, max_length=10, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='nuser',
            name='reject_reason',
            field=models.TextField(blank=True, verbose_name='拒绝原因'),
        ),
    ]
