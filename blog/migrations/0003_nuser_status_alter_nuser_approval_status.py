# Generated by Django 4.2.3 on 2023-07-17 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_nuser_username_alter_nuser_identity_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nuser',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '正常'), (-1, '拉黑')], default=0, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='nuser',
            name='approval_status',
            field=models.SmallIntegerField(choices=[(1, 'PASS'), (0, 'NO_APPROVAL'), (3, 'WAIT'), (2, 'REJECT')], default=0, verbose_name='审核状态'),
        ),
    ]
