from django.db import models

# Create your models here.
class ProjectsModels(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=60, verbose_name='项目名称', help_text='项目名称', unique=True)
    leader = models.CharField(max_length=100, verbose_name='项目负责人', help_text='项目负责人')
    # leader_phone = models.CharField(max_length=20, verbose_name='项目负责人电话', help_text=' ', blank=True, null=True)
    tester = models.CharField(max_length=200, verbose_name='测试人员', help_text='测试人员', blank=True, null=True)
    programmer = models.CharField(max_length=200, verbose_name='开发人员', help_text='开发人员', blank=True, null=True)
    # project_states = models.CharField(max_length=5, verbose_name='项目状态', help_text='结束:0;进行中:1;暂停:2')
    desc = models.TextField(verbose_name='项目简介', help_text='项目简介', default='暂无简介', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        db_table = 'tb_projects'
        verbose_name = '项目信息'
        # 数据库模型类的复数，apple -> apples
        verbose_name_plural = verbose_name