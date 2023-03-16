# Generated by Django 3.2.17 on 2023-03-10 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterfacesModels',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='所属接口', max_length=60, verbose_name='所属接口')),
                ('interfaces_states', models.CharField(help_text='结束:0;进行中:1;暂停:2', max_length=5, verbose_name='接口状态')),
                ('tester', models.CharField(help_text='测试人员', max_length=50, verbose_name='测试人员')),
                ('desc', models.CharField(blank=True, help_text='简要描述', max_length=200, null=True, verbose_name='简要描述')),
                ('apps', models.ForeignKey(help_text='所属软件', on_delete=django.db.models.deletion.CASCADE, related_name='apps', to='apps.appsmodels', verbose_name='所属软件')),
            ],
            options={
                'verbose_name': '接口信息',
                'verbose_name_plural': '接口信息',
                'db_table': 'tb_interfaces',
            },
        ),
    ]