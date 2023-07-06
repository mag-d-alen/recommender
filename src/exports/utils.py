import csv
from django.apps import apps
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
import tempfile

from ratings.models import Rating



def generate_rating_dataset(app_label = 'movies', model='movie'):
    ctype = ContentType.objects.get(app_label=app_label, model=model)
    qs = Rating.objects.filter(active = True, content_type = ctype)
    qs = qs.annotate(userId = F('user_id'), movieId=F('object_id'), rating=F('value'))
    return qs.values('userId', 'movieId', 'rating')

def export_dataset(app_label = 'movies', model='movie'):
    Export = apps.get_model('exports', 'Export')
    with tempfile.NamedTemporaryFile(mode = 'r+') as temp_file:
        dataset = generate_rating_dataset(app_label=app_label, model=model)
        try:
            keys= dataset[0].keys()
        except:
            return
        dict_writer = csv.DictWriter(temp_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataset)
        temp_file.seek(0) #go to top of the file
        obj = Export.objects.create()
        obj.file.save('export.csv', File(temp_file))
        
        
            

        
    