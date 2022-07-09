# 参考：https://www.celerycn.io/jian-jie
# celery 分布式任务队列
# worker
# broker
# 需要消息中间件来进行发送和接收消息，RabbitMQ，Redis，Sqlite
from celery import Celery
app = Celery('hello', broker='amqp://guest@localhost//')
@app.task
def hello():
    return 'hello world'
# 优点：简单，高可用，快速，灵活，
# 支持：中间人，结果存储，并发，序列化
# 功能：监控，调度，工作流，资源（内存）泄漏保护，时间和速率的限制，自定义组件

# 安装
# pip install -U Celery
# pip install "celery[librabbitmq]"
# pip install "celery[librabbitmq,redis,auth,msgpack]"
# 序列化，并发，传输和后端

# *********************************************************************************************************************
# https://www.celerycn.io/ru-men/zhong-jian-ren-brokers/shi-yong-rabbitmq#mac-os-an-zhuang-rabbitmq
# 使用rabbitmq
# broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
# 安装rabbitmq服务
# 配置rabbitmq
# sudo rabbitmqctl add_user myuser mypassword
# sudo rabbitmqctl add_vhost myvhost
# sudo rabbitmqctl set_user_tags myuser mytag
# sodo rabbotmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
# Mac OS安装的rabbitmq
# sudo ruby -e "$(curl -fsSL http://raw.githubusercontent.com/Homebrew/install/master/install)"
# brew install rabbitmq
# PATH=$PATH:/usr/local/sbin
# 配置系统名称
# sudo scutil --set myhost myhost.local
# 127.0.0.1 localhost myhost myhost.local
# rabbitmqctl status
# 启动/停止rabbitmq服务
# sudo rabbitmqctl-server
# sudo rabbitmqctl-server -detached
# sudo rabbitmqctl stop

# *********************************************************************************************************************
# https://www.celerycn.io/ru-men/zhong-jian-ren-brokers/shi-yong-redis
# 使用redis
# 安装
# pip install -U "celery[redis]"
# 配置
# app.conf.broker_url = 'redis://localhost:6379/0'
# redis://password@hostname:port/db_number
# redis+socket:///path/to/redis.sock
# redis+socket:///path/to/redis.sock?virtual_host=db_number
# app.conf.broker_url = 'sentinel:localhost:26379;sentinel://localhost:26380;sentinel://localhost:26381'
# app.conf.broker_transport_options = {'master_name':'clusterl'}
# 可见性超时
# app.conf.broker_transport_options = {'visibility_timeout': 3600} # 一个小时
# 结果
# app.conf.result_backend = 'redis://localhost:7379/0'
# app.conf.result_backend_transport_options = {'master_name': "mymaster"}
# 注意事项
# 广播前缀
# app.conf.broker_transport_options = {'fanout_prefix': true}
# 广播模式
# app.conf.broker_transport_options = {'fanout_patterns': true}
# 可见性超时
# app.conf.broker_transport_options = {'visibility_timeout': 432000}
# 驱逐key

# *********************************************************************************************************************
# https://www.celerycn.io/ru-men/celery-chu-ci-shi-yong
# Celery初次使用
# 选择中间人broker
# rabbitmq
# 使用rabbitmq
# ubuntu:
# sudo apt-get install rabbitmq-server
# docker
# docker run -d -p 5462:5462 rabbitmq
# Redis
# 使用redis:
# docker run -d -p 6379:6379 redis
# 其他中间件：Amazon SQS

# 安装celery
# pip install celery
# 应用
#























