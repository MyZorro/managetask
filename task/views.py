# coding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from task.models import Edition, Product, Task, Person, Actor
from django.db.models import Q
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def login(request):
    if request.is_ajax():
        data = json.loads(request.body.decode("utf-8"))
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = user.first_name
            request.session['user_id'] = user.id
            # response = HttpResponseRedirect('/task/edition_manage')
            response = JsonResponse({"status": 1200, "message": "登录成功"})
            return response
        else:
            return JsonResponse({"status": 1301, "message": "账户名或密码错误"})
    else:
        return render(request, 'task/login.html')


@login_required
def edition_manage(request):  # 项目列表
    username = request.session.get('user')
    userid = request.session.get('user_id')
    print(userid, username)
    edition_data = Edition.objects.filter(status__gt=0).order_by('-createTime')
    data = []
    for i in edition_data:
        edition_dict = {'projectName': i.projectName, 'editionNum': i.editionNum, 'environment': i.environment,
                        'createTime': i.createTime, 'status': i.status, 'downloadLink': i.downloadLink, 'id': i.id}
        data.append(edition_dict)
    return render(request, 'task/edition_manage.html', {'user': username, 'personid': str(userid), 'edition_list': data})


@login_required
def add_edit_button(request, edition_id, flag):  # 新增、查看或者修改版本
    # print(edition_id, flag)
    if request.method == "POST":
        projectName = request.POST.get('projectName', '')
        editionNum = request.POST.get('editionNum', '')
        environment = request.POST.get('environment', '')
        downloadLink = request.POST.get('downloadLink', '')
        describe = request.POST.get('describe', '')
        if str(edition_id) == '0':  # 新增提交表单
            Edition.objects.create(projectName=projectName,
                                   editionNum=editionNum,
                                   environment=environment,
                                   status=1,
                                   downloadLink=downloadLink,
                                   describe=describe
                                   )
            response = HttpResponseRedirect('/task/edition_manage')
            return response
        else:  # 修改提交表单
            edition_info = Edition.objects.get(pk=edition_id)
            # print(edition_info)
            if edition_info.status == 1:
                edition_info.projectName = projectName
                edition_info.editionNum = editionNum
                edition_info.environment = environment
                edition_info.downloadLink = downloadLink
                edition_info.describe = describe
                edition_info.save()
                response = HttpResponseRedirect('/task/edition_manage')
                return response
            else:
                return render(request, 'task/add_edition.html', {'edition_list': edition_info,
                                                                 'error': '正在测试或测试完成的不能修改！'})
    else:
        product_list = Product.objects.all()
        prodata = []
        for i in product_list:
            product_dict = {"product_name": i.Product_name, "status": i.status}
            prodata.append(product_dict)
        if edition_id == '0':  # 新增
            return render(request, 'task/add_edition.html', {'product_list': prodata, "isList": "1"})
        else:
            edition_data = Edition.objects.get(pk=edition_id)
            edition_dict = {'projectName': edition_data.projectName, 'editionNum': edition_data.editionNum,
                            'environment': edition_data.environment, 'status': edition_data.status, 'downloadLink':
                                edition_data.downloadLink, 'describe': edition_data.describe, 'id': edition_data.id}
            if flag == '0':  # 查看
                return render(request, 'task/add_edition.html', {'edition_list': edition_dict, "isSub": "0"})
            else:  # 修改
                return render(request, 'task/add_edition.html',
                              {'edition_list': edition_dict, 'product_list': prodata, "isList": "1"})


@login_required
def delete_project(request, edition_id):  # 删除版本
    edition_info = Edition.objects.get(pk=edition_id)
    if edition_info.status == 2:
        return render(request, 'task/add_edition.html', {'error': '正在测试或测试完成的不能修改！'})
    else:
        edition_info.status = 0
        edition_info.save()
        response = HttpResponseRedirect('/task/edition_manage')
        return response


@login_required
def search_edition(request):  # 查询
    if request.method == "POST":
        username = request.session.get('user')
        project_name = request.POST.get('project_name', '')
        environment = request.POST.get('environment', '')
        editstatus = request.POST.get('editstatus', '')
        # print(project_name, environment, type(editstatus))
        if project_name == '':
            if environment != "-1" and editstatus == "-1":
                # print(environment, editstatus)
                edition_name = Edition.objects.filter(environment=environment)
                return render(request, 'task/edition_manage.html', {'username': username, 'edition_list': edition_name})
            elif environment == '-1' and editstatus != "-1":
                edition_name = Edition.objects.filter(status=editstatus)
                return render(request, 'task/edition_manage.html', {'username': username, 'edition_list': edition_name})
            elif environment != '-1' and editstatus != "-1":
                edition_name = Edition.objects.filter(Q(status=editstatus) & Q(environment=environment))
                return render(request, 'task/edition_manage.html', {'username': username, 'edition_list': edition_name})
            else:
                edition_name = Edition.objects.all()
                return render(request, 'task/edition_manage.html', {'username': username, 'edition_list': edition_name})
        else:
            if environment == "-1" and editstatus == "-1":
                edition_name = Edition.objects.filter(projectName__icontains=project_name)
                return render(request, 'task/edition_manage.html', {'username': username, 'edition_list': edition_name})
            elif environment != "-1" and editstatus == "-1":
                # print(environment, editstatus)
                edition_name = Edition.objects.filter(Q(projectName__icontains=project_name) & Q(environment=environment))
                # edition_env = Edition.objects.filter(environment=environment)
                return render(request, 'task/edition_manage.html', {'username': username, 'edition_list': edition_name})
            elif environment == '-1' and editstatus != "-1":
                edition_name = Edition.objects.filter(Q(projectName__icontains=project_name) & Q(status=editstatus))
                return render(request, 'task/edition_manage.html', {'username': username, 'edition_list': edition_name})
            else:
                edition_name = Edition.objects.filter(Q(projectName__icontains=project_name) & Q(status=editstatus) &
                                                      Q(environment=environment))
                return render(request, 'task/edition_manage.html', {'username': username, 'edition_list': edition_name})


@login_required
def task_manage(request):  # 测试任务列表
    username = request.session.get('user')
    personid = request.session.get('person_id')
    task_list = Task.objects.filter(task_status__gt=0).order_by('-createTime')
    taskdata = []
    for i in task_list:
        actid = []
        actidlt = Actor.objects.filter(task_id=i.id)
        for m in actidlt:
            actid.append(m.actorId)
        task_dict = {"taskName": i.taskName, "editionNum": i.edition.editionNum, 'environment': i.edition.environment,
                     'createTime': i.createTime, 'task_status': i.task_status, 'lastTime': i.lastTime, 'downloadLink':
                         i.edition.downloadLink, 'edition_id': i.edition.id, 'id': i.id, "actor": actid}
        taskdata.append(task_dict)
    return render(request, 'task/task_manage.html', {'personid': str(personid), 'user': username, 'task_list': taskdata})


@login_required
def add_task(request, edition_id, task_id, flag):  # 新增或者修改任务
    if request.method == "POST":
        taskname = request.POST.get('taskName', '')
        describe = request.POST.get('describe', '')
        personid = request.POST.getlist('person_Name')
        print(edition_id, task_id, flag, personid)
        if str(task_id) == '0':  # 新增提交表单
            # print(edition_id, task_id, flag, personname)
            Task.objects.create(taskName=taskname, task_status=2, task_describe=describe, edition_id=edition_id)  # 新建任务
            edition_info = Edition.objects.get(pk=edition_id)  # 改版本的状态
            edition_info.status = 2
            edition_info.save()
            tid = Task.objects.get(edition_id=edition_id)
            for i in personid:
                Actor.objects.create(actorId=str(i), task_id=tid.id)
            response = HttpResponseRedirect('/task/task_manage')
            return response
        else:  # 修改提交表单
            print(edition_id, task_id, flag, personid)
            tk_if = Task.objects.get(pk=task_id)
            # print(edition_info)
            if tk_if.task_status == 2:
                tk_if.taskName = taskname
                tk_if.task_describe = describe
                Actor.objects.filter(task_id=task_id).delete()
                for i in personid:
                    Actor.objects.create(actorId=str(i), task_id=task_id)
                tk_if.save()
                response = HttpResponseRedirect('/task/task_manage')
                return response
            else:  # 该处点提交 提示后 页面有些字段没有填充，影响不大懒得管了
                return render(request, 'task/add_task.html', {'edition_info': tk_if, 'error': '正在测试或测试完成的不能修改！'})
    else:
        edition_info = Edition.objects.get(pk=edition_id)
        # print(edition_info.id)
        if task_id == '0':  # 新增任务
            check_task = {'name': [], 'environment': edition_info.environment, 'editionNum': edition_info.editionNum,
                          'downloadLink': edition_info.downloadLink, 'edition_id': edition_info.id, 'task_id': 0}
            p_name = Person.objects.filter(status=1)
            for i in p_name:
                check_task["name"].append(i)
            return render(request, 'task/add_task.html', {'edition_info': check_task})
        else:
            task_info = Task.objects.get(pk=task_id)
            act = Actor.objects.filter(task_id=task_id)
            check_task = {'taskName': task_info.taskName, "task_describe": task_info.task_describe, 'name': [],
                          'environment': edition_info.environment, 'editionNum': edition_info.editionNum, 'downloadLink':
                              edition_info.downloadLink, 'edition_id': edition_info.id, 'task_id': task_info.id}
            for i in act:
                n = Person.objects.get(pk=i.actorId)
                check_task["name"].append(n)
            # print(name)
            if flag == '0':  # 查看任务
                return render(request, 'task/add_task.html', {'edition_info': check_task, "isSub": "0"})
            else:  # 修改任务
                check_task = {'taskName': task_info.taskName, "task_describe": task_info.task_describe, 'name': [],
                              'environment': edition_info.environment, 'editionNum': edition_info.editionNum,
                              'downloadLink':
                                  edition_info.downloadLink, 'edition_id': edition_info.id, 'task_id': task_info.id}
                p_name = Person.objects.filter(status=1)
                for i in p_name:
                    check_task["name"].append(i)
                return render(request, 'task/add_task.html', {'edition_info': check_task})


@login_required
def delete_task(request):  # 删除任务
    pass


@login_required
def search_task(request):  # 查询任务
    if request.method == "POST":
        username = request.session.get('user')
        task_name = request.POST.get('task_name', '')
        environment = request.POST.get('environment', '')
        editstatus = request.POST.get('editstatus', '')
        if task_name == '':
            if environment != "-1" and editstatus == "-1":  # 单查环境
                edition_name = Edition.objects.filter(environment=environment).order_by('-createTime')
                editionid = []
                tasklt = []
                for i in range(len(edition_name)):
                    print(len(edition_name))
                    editionid.append(edition_name[i].id)
                    print(edition_name[i].id)
                    task11 = Task.objects.filter(edition_id=edition_name[i].id)
                    print(task11)
                    tasklt.append(task11[0].edition_id)
                insec = list(set(editionid).intersection(set(tasklt)))
                print(insec)
                task_dict = {"taskName": task11.taskName, "editionNum": task11.edition.editionNum, 'environment': task11.edition.environment,
                             'createTime': task11.createTime, 'task_status': task11.task_status, 'lastTime': task11.lastTime, 'downloadLink':
                                 task11.edition.downloadLink, 'edition_id': task11.edition.id, 'id': task11.id}
                tasklt.append(task_dict)
                return render(request, 'task/task_manage.html', {'username': username, 'task_list': tasklt})
            elif environment == '-1' and editstatus != "-1":  # 单查状态
                task_name = Task.objects.filter(task_status=editstatus).order_by('-createTime')
                tasklt = []
                for i in task_name:
                    task_dict = {"taskName": i.taskName, "editionNum": i.edition.editionNum,
                                 'environment': i.edition.environment,
                                 'createTime': i.createTime, 'task_status': i.task_status,
                                 'lastTime': i.lastTime, 'downloadLink':
                                     i.edition.downloadLink, 'edition_id': i.edition.id, 'id': i.id}
                    tasklt.append(task_dict)
                return render(request, 'task/task_manage.html', {'username': username, 'task_list': tasklt})
            elif environment != '-1' and editstatus != "-1":  # 环境状态一起
                edition_name = Edition.objects.filter(environment=environment).order_by('-createTime')
                tasklt = []
                for i in edition_name:
                    task11 = Task.objects.get(edition_id=i.id)
                    if str(task11.task_status) == str(editstatus):
                        task_dict = {"taskName": task11.taskName, "editionNum": task11.edition.editionNum,
                                     'environment': task11.edition.environment,
                                     'createTime': task11.createTime, 'task_status': task11.task_status,
                                     'lastTime': task11.lastTime, 'downloadLink':
                                         task11.edition.downloadLink, 'edition_id': task11.edition.id, 'id': task11.id}
                        tasklt.append(task_dict)
                    else:
                        continue
                return render(request, 'task/task_manage.html', {'username': username, 'task_list': tasklt})
            else:  # 三个都为空查询
                task_list = Task.objects.filter(task_status__gt=0).order_by('-createTime')
                tasklt = []
                for i in task_list:
                    task_dict = {"taskName": i.taskName, "editionNum": i.edition.editionNum,
                                 'environment': i.edition.environment,
                                 'createTime': i.createTime, 'task_status': i.task_status, 'lastTime': i.lastTime,
                                 'downloadLink':
                                     i.edition.downloadLink, 'edition_id': i.edition.id, 'id': i.id}
                    tasklt.append(task_dict)
                return render(request, 'task/task_manage.html', {'username': username, 'task_list': tasklt})
        else:
            if environment == "-1" and editstatus == "-1":  # 单查名称
                task_inf = Task.objects.filter(taskName__icontains=task_name).order_by('-createTime')
                tasklt = []
                for i in task_inf:
                    task_dict = {"taskName": i.taskName, "editionNum": i.edition.editionNum,
                                 'environment': i.edition.environment,
                                 'createTime': i.createTime, 'task_status': i.task_status, 'lastTime': i.lastTime,
                                 'downloadLink':
                                     i.edition.downloadLink, 'edition_id': i.edition.id, 'id': i.id}
                    tasklt.append(task_dict)
                return render(request, 'task/task_manage.html', {'username': username, 'task_list': tasklt})
            elif environment != "-1" and editstatus == "-1":  # 查名称且环境
                edition_name = Edition.objects.filter(environment=environment).order_by('-createTime')
                print(edition_name)
                tasklt = []
                for i in edition_name:
                    if i.status !=1:
                        pass
                    task11 = Task.objects.get(edition_id=i.id)
                    if task_name in task11.taskName:
                        task_dict = {"taskName": task11.taskName, "editionNum": task11.edition.editionNum,
                                     'environment': task11.edition.environment,
                                     'createTime': task11.createTime, 'task_status': task11.task_status,
                                     'lastTime': task11.lastTime, 'downloadLink':
                                         task11.edition.downloadLink, 'edition_id': task11.edition.id, 'id': task11.id}
                        tasklt.append(task_dict)
                    else:
                        continue
                return render(request, 'task/task_manage.html', {'username': username, 'task_list': tasklt})
            elif environment == '-1' and editstatus != "-1":
                edition_name = Edition.objects.filter(Q(taskName__icontains=task_name) & Q(status=editstatus))
                return render(request, 'task/task_manage.html', {'username': username, 'task_list': edition_name})
            else:
                edition_name = Edition.objects.filter(Q(taskName__icontains=task_name) & Q(status=editstatus) &
                                                      Q(environment=environment))
                return render(request, 'task/task_manage.html', {'username': username, 'task_list': edition_name})


@login_required
def logout(request):
    return render(request, 'task/login.html')
