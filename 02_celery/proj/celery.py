# https://www.celerycn.io/ru-men/celery-jin-jie-shi-yong

from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery(
    'proj',
    broker='amqp://',
    backend='amqp://',
    include=['proj.tasks']
)
# Optional configureation, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()