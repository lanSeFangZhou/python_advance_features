# https://www.celerycn.io/ru-men/celery-chu-ci-shi-yong
from celery import Celery
# 第一个参数：当前模块的名称，只有在__main__模块中定义任务时才会生产名称
# 第二个参数：中间人(broker)的链接url，实例中使用的rabbitmq(celery默认使用的也是rabbitmq)
# rabbitmq可以写成：amqp://localhost, redis可以写成：redis://localhost
app = Celery('tasks', broker='amqp://guest@localhost//')
@app.task
def add(x, y):
    return x + y

# 运行Celery职程(worker)服务
# celery -A tasks worker --loglevel=info
# 命令帮助：
# celery worker --help
# celery help

# 调用任务
# from tasks import add
# add.delay(4, 4)

# 保存结果
# RPC作为结果后端
# app = Celery('tasks', backend='rpc://', broker='pyamqp://')
# Redis作为结果后端
# app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')
# result = add.delay(4, 4)
# 检测结果是否处理完毕
# result.ready()
# 异步转换为同步调用
# result.get(timeout=1)
# 任务出现异常
# result.get(propagate=False)
# 回溯
# result.traceback

# 配置
# app.conf.task_serializer = 'json'
# app.conf.update(
#   task_serializer='json',
#   accept_content=['json'], # Ignore other content
#   result_serializer='json',
#   timezone='Europe/Oslo',
#   enable_utc=True,
# )

# 加载配置模块
# app.config_from_object('celeryconfig')
# 创建一个celeryconfig.py的文件，添加以下内容：
# broker_url = 'pyamqp://'
# result_backend = 'rpc://'
# task_serializer = 'json'
# result_serializer = 'json'
# accept_content = ['json']
# timezone = 'Europe/Oslo'
# enable_utc = True

# 验证配置模块是否配置正确
# python -m celeryconfig

# 设置任务执行错误时的专用队列中
# celeryconfig.py
# task_routes = {
#   'tasks.add': 'low_priority',
# }

# 针对任务进行限速，以下为每分钟内允许执行的10个任务的配置
# celeryconfig.py
# task_annotations = {
#   'tasks.add': {'rate_limit': '10/m'},
# }

# 如果使用的是RabbitMQ或者Redis,可以在运行时进行设置任务的速率：
# celery -A tasks control rate_limit tasks.add 10/m

# 故障处理
# 职程(worker)无法正常启动：权限错误
# ln -s /run/shm /dev/shm

# 任务总处于pending(待处理)状态
# result = task.delay(...)
# print(result.backend)
















