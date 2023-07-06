from celery import shared_task


from exports.utils import export_dataset, generate_rating_dataset

@shared_task(name='export_rating_dataset')
def export_rating_dataset_task():
    export_dataset()