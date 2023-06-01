from django.db import models

# Create your models here.


class InterfacesModels(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey('projects.ProjectsModels', on_delete=models.CASCADE,
                                 verbose_name='所属项目', help_text='所属项目', related_name='interfaces')
    name = models.CharField(max_length=60, verbose_name='所属接口', help_text='所属接口')
    # interfaces_states = models.CharField(max_length=5, verbose_name='接口状态', help_text='结束:0;进行中:1;暂停:2')
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField(verbose_name='简要描述', max_length=200, null=True, blank=True, help_text='简要描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        db_table = 'tb_interfaces'
        verbose_name = '接口信息'
        # 数据库模型类的复数，apple -> apples
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name