from __future__ import absolute_import, unicode_literals
from .celery import app

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)

# 运行职程
# celery -A proj worker -l info
# 运行时，会有日志：
# broker为celery程序中指定的中间人broker的连接URL，也可以通过 -b 选项在命令行进行设置其他的中间人broker
# concurrency为同时处理任务的工作进程数量，所有的进程都被占满时，新的任务需要进行等待其中的一个进程完成任务
# 才能执行进行任务。
# 默认的并发数为当前计算机的CPU数，可以通过设置celery worker-c 项进行自定义设置并发数。没有推荐的并发数，因为
# 最佳的并发数取决于很多因素，如果任务主要是I/O限制，可以进行增加并发数，经过测试，设置超过两倍的CPU数量效果不是
# 很好，很有可能会降低性能。
# 包括默认的prefork池，celery也支持在单个线程池中使用eventlet,gevent：
# Events选项设置为启动状态时，celery会开启监控事件来进行监视职程(worker)。一般情况用于监控程序，如flower和实
# 时celery监控；
# Queues为职程(worker)任务队列，可以告诉职程(worker)同时从多个任务中进行消费。通常用于将任务消息路由到特定的
# 职程(worker)、提升服务质量、关注点分离、优先级排序的常用手段。
# help
# celery worker --help

# 停止职程
# ctrl + c
# 后台运行
# 守护进程：Daemonization
# 使用celery multi命令在后台启动一个或多个职程(worker)
# celery multi start w1 -A proj -l info
# 重启：
# celery multi restart w1 -A proj -l info
# 停止运行
# celery multi stop w1 -A proj -l info
# stop命令是异步的，所以不会等待职程(worker)关闭。可以通过stopwait命令进行停止运行，可以保证在退出之前完成当前正在执行的任务：
# celery multi stopwait w1 -A proj -l info

# 注意：celery multi 不存储有关职程(worker)的信息，所以在重新启动时需要使用相同的命令参数，停止运行时只能通过pidfile和logfile
# 参数来进行停止运行。

# 默认情况下会在当前目录中创建pid文件和日志文件，为防止多个职程(worker)干扰，建议将这些文件存放在专门的目录中：
# mkdir -p /var/run/celery
# mkdir -p /var/log/celery
# celery multi start w1 -A proj -l info --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log

# 也可以使用multi命令启动多个职程(worker)，有一个强大的语法为不同职程(worker)设置不同的参数：
# celery multi start 10 -A proj -l info -Q:1-3 images,vedio -Q:4,5 data -Q default -L:4,5 debug

# 关于--app参数
# 使用--app参数可以指定运行的celery应用程序实例，格式必须为 module.path:atribute
# 但如果只设置包名，它将进行搜索app实例，顺序如下：
# 用--app=proj:
# 1.名为proj.app的属性
# 2.名为proj.celery的属性
# 3.模块proj中值为celery应用程序的任何属性，如果还没找到，将尝试检索名为proj.celery的子模块
# 4.名为proj.celery.app的属性
# 5.名为proj.celery.celery的属性
# 6.模块proj.celery中值为celery应用程序的任何属性
# 7.在此方案模仿文档中使用的实例，即针对单个模块包含的proj:app，以及大型项目的proj.celery:app

# 程序调用
# add.delay(2, 2)
# add.apply_async((2, 2))
# add.apply_async((2, 2), queue='lopri', countdown=10)
# add(2, 2)

# 默认情况下禁用结果。如果配置了结果后端，可以获取任务的返回值：
# res = add.delay(2, 2)
# res.get(timeout=1)
# 通过id属性进行获取任务的id：
# res.id
# 如果任务引发异常，可以进行检查异常及溯源，默认情况下result.get()会抛出异常
# res = add.delay(2)
# res.get(timeout=1)

# 如果不希望celery抛出异常，可以通过设置propagate来进行禁用：
# res.get(propagate=False)
# res.failed()
# res.successful()
# res.state

# 一个任务只能有当前一个状态，但他的执行过程可以为过个状态
# 启动状态是一种比较特殊的状态，仅在task_track_started启动设置或@task(track_started=True)的情况下才会进行记录
# 挂起状态实际上不是记录状态，而是未知任务ID的默认状态
# from proj.celery import app
# res = app.AsyncResult('this-id-does-not-exist')
# res.state
# 任务的阶段为：
# PENDING-》STATED-》RETRY-》STARTED-》RETRY-》STATED-》SUCCESS

# Canvas：设计工作流程
# add.signature((2, 2), countdown=10)
# add.s(2, 2)

# 再次调用api
# s1 = add.s(2, 2)
# res = s1.delay()
# res.get()
# s2 = add.s(2)
# res = s2.delay(8)
# res.get()
# s3 = add.s(2, 2, debug=True)
# s3.delay(debug=False)

# 组：Groups
# from celery import group
# from proj.tasks import add
# group(add.s(i, i) for i in xrange(10))().get()
# g = group(add.s(i) for i in xrange(10))
# g(10).get()

# 链：chains
# from celery import chain
# from proj.tasks import add, mul
# chain(add.s(4, 4) | mul.s(8))().get()
# # (? + 4) * 8
# g = chain(add.s(4) | mul.s(8))
# g(4).get()
# (add.s(4, 4) | mul.s(8))().get()

# 和弦：chords
# 和弦是一个带有回调的组：
# from celery import chord
# from proj.tasks import add, xsum
# chord((add.s(i, i) for i in xrange(10)), xsum.s())().get()
# 链接到其他任务的组将自动转换为和弦：
# (group(add.s(i, i) for i in xrange(10)) | xsum.s())().get()
# upload_document.s(file) | group(apply_filter.s() for filter in filters)

# 路由
# app.conf.update(
#   task_routes = {
#       'proj.tasks.add':{'queue':'hipri'},
#   },
# )

# 使用queue参数进行指定队列
# from proj.tasks import add
# add.apply_async((2, 2), queue='hipri')
# 可以通过设置运行职程(worker)时指定职程(worker)从某个队列中进行消费(celery worker -Q)
# celery -A proj worker -Q hipri
# celery -A proj worker -Q hipri,celery


# 远程控制
# celery -A proj inspect active
# celery -A proj inspect active --destination=celery@example.com
# celery -A proj control --help
# celery -A proj control enable_events
# celery -A proj events --dump
# celery -A proj events
# celery -A proj control disable_events
# celery -A proj status


# 时区
# app.conf.timezone = 'Europe/London'
# 优化
# pip install librabbitmq
























