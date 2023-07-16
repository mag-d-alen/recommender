from celery import shared_task


from exports.utils import generate_movie_dataset, generate_rating_dataset

@shared_task(name='export_rating_dataset')
def export_rating_dataset_task():
    generate_rating_dataset()


@shared_task(name='export_movie_dataset')
def export_movie_dataset_task():
    generate_movie_dataset(to_csv=True)