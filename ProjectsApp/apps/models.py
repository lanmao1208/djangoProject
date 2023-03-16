from django.db import models

# Create your models here.
class AppsModels(models.Model):
    id = models.AutoField(primary_key=True)
    projects = models.ForeignKey('projects.ProjectsModels', on_delete=models.CASCADE,
                                 verbose_name='所属项目', help_text='所属项目', related_name='interfaces')
    name = models.CharField(max_length=60, verbose_name='所属软件', help_text='所属软件')
    apps_states = models.CharField(max_length=5, verbose_name='软件运行状态', help_text='结束:0;进行中:1;暂停:2')
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField(verbose_name='简要描述', max_length=200, null=True, blank=True, help_text='简要描述')

    class Meta:
        db_table = 'tb_apps'
        verbose_name = '软件信息'
        # 数据库模型类的复数，apple -> apples
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name