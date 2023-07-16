import csv
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
import tempfile
from exports.models import Export, ExportDataTypes
from movies.models import Movie

from ratings.models import Rating


def export_dataset(dataset, fname, type):
    with tempfile.NamedTemporaryFile(mode='r+') as temp_file:
        try:
            keys = dataset[0].keys()
        except:
            return
        dict_writer = csv.DictWriter(temp_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataset)
        temp_file.seek(0)  # go to top of the file
        obj = Export.objects.create(type=type)
        obj.file.save(fname, File(temp_file))


def generate_rating_dataset(app_label='movies', model='movie', to_csv=True):
    ctype = ContentType.objects.get(app_label=app_label, model=model)
    qs = Rating.objects.filter(active=True, content_type=ctype)
    qs = qs.annotate(userId=F('user_id'), movieId=F(
        'object_id'), rating=F('value'))
    dataset = qs.values('userId', 'movieId', 'rating')
    if to_csv:
        export_dataset(dataset=dataset, fname='ratings.csv',
                       type=ExportDataTypes.RATINGS)
    return dataset


def generate_movie_dataset(to_csv=True):
    qs = Movie.objects.all()[:250]
    qs = qs.annotate(movieId=F('id'), movieIdx=F('idx'))
    dataset = qs.values( 'movieIdx','movieId', 'title',
                        'release_date', 'rating_count', 'rating_avg')
    if to_csv:
        export_dataset(dataset, fname='movies.csv', type=ExportDataTypes.MOVIES)
    return dataset
