from celery import shared_task


@shared_task(name='new_task')
def new_task():
    """новая задача."""
    print('новая задача')
    return "новая задача -- ok"
