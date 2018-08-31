from django.conf import settings
from django.db import models


class Person(models.Model):
    STATUS_CHOICES = (
        ('1', '产品'),
        ('2', 'UI'),
        ('3', '开发'),
        ('4', '测试'),
        ('5', '其他'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=3, choices=STATUS_CHOICES, default='4')
    modify_time = models.DateField(verbose_name='修改时间', auto_now=True, null=True)

    def __str__(self):
        return self.position


def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = Person()
        profile.user = instance
        profile.save()


class Product(models.Model):
    Product_name = models.CharField(null=True, max_length=15, verbose_name='项目名称')
    Product_describe = models.TextField(null=True, max_length=100, verbose_name='项目描述')
    status = models.SmallIntegerField(verbose_name='状态')

    def __str__(self):
        return self.Product_name


class Edition(models.Model):
    projectName = models.CharField(max_length=20)
    editionNum = models.CharField(max_length=20)
    environment = models.CharField(max_length=8)
    createTime = models.DateField(auto_now_add=True)
    status = models.SmallIntegerField()
    downloadLink = models.URLField(max_length=100)
    describe = models.TextField(max_length=200)

    def __str__(self):
        return self.projectName


class Task(models.Model):
    edition = models.OneToOneField('Edition', on_delete=models.CASCADE)
    taskName = models.CharField(max_length=20)
    createTime = models.DateField(auto_now_add=True)
    lastTime = models.DateField(auto_now=True)
    task_status = models.SmallIntegerField(default=1)
    task_describe = models.TextField(max_length=300)
    act_persons = models.ManyToManyField(
        Person,
        through='Actor',  # 自定义中间表
        through_fields=('task', 'person'),
    )

    def __str__(self):
        return self.taskName


class Actor(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, null=True)
    act_status = models.SmallIntegerField(default=0)
    task_describe = models.TextField(max_length=200)

    def __str__(self):
        return self.person
