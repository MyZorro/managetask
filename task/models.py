from django.db import models


class Person(models.Model):
    person_name = models.CharField(max_length=20, verbose_name='姓名')
    position = models.IntegerField()
    email = models.EmailField(verbose_name='邮箱')
    create_time = models.DateTimeField(auto_now=True)
    modify_time = models.DateTimeField(verbose_name='修改时间', null=True)
    status = models.IntegerField(verbose_name='状态')

    def __str__(self):
        return self.person_name


class Product(models.Model):
    Product_name = models.CharField(default='', max_length=20, verbose_name='项目名称')
    Product_describe = models.TextField(default='', max_length=300, verbose_name='项目描述')
    status = models.IntegerField(verbose_name='状态')

    def __str__(self):
        return self.Product_name


class Edition(models.Model):
    projectName = models.CharField(max_length=30)
    editionNum = models.CharField(max_length=50)
    environment = models.CharField(max_length=20)
    createTime = models.DateTimeField(auto_now=True)
    status = models.IntegerField()
    downloadLink = models.CharField(max_length=100)
    describe = models.TextField(max_length=200)

    def __str__(self):
        return self.projectName


class Task(models.Model):
    edition = models.ForeignKey('Edition')
    taskName = models.CharField(max_length=30)
    createTime = models.DateTimeField(auto_now=True)
    lastTime = models.DateTimeField(auto_now=True)
    task_status = models.IntegerField(default=1)
    task_describe = models.TextField(max_length=300)

    def __str__(self):
        return self.taskName


class Actor(models.Model):
    task = models.ForeignKey('Task')
    actorId = models.CharField(max_length=5)
    act_status = models.IntegerField(default=0)
    task_describe = models.TextField(max_length=200)

    def __str__(self):
        return self.actorId
