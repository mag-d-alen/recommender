import pickle
import tempfile
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import File
from exports import storages
from ratings.models import Rating
from surprise import accuracy, Reader,Dataset, SVD
from surprise.model_selection import cross_validate
from django.conf import settings


def export_ratings_dataset():
    ctype = ContentType.objects.get(app_label = 'movies', model = 'movie')
    qs = Rating.objects.filter(active=True, content_type = ctype).annotate(userId = F('user_id'), movieId= F('object_id'), rating= F('value'))
    return qs.values('userId', 'movieId', 'rating')


def get_data_loader(dataset, columns =['userId', 'movieId', 'rating']):
    import pandas as pd
    df = pd.DataFrame(dataset)
    df['rating'].dropna(inplace = True)
    max_rating, min_rating = df['rating'].max(), df['rating'].min()
    reader = Reader(rating_scale=(min_rating, max_rating))
    return Dataset.load_from_df(df[columns], reader)

def get_model_accuracy(trainset, model, use_rmse = True, verbose =True):
    testset = trainset.build_testset()
    predictions = model.test(testset)
    #RMSE should be low
    acc = accuracy.rmse(predictions, verbose=verbose)
    if not use_rmse:
        return acc.mae(predictions, verbose=verbose)
    return acc

def train_model(n_epochs=20, verbose=True):
    dataset = export_ratings_dataset()
    loaded_data= get_data_loader(dataset)
    model = SVD(verbose =True, n_epochs=n_epochs)
    cv_results = cross_validate(model, loaded_data, measures = ['RMSE','MAE'], cv=4, verbose=verbose)# only for manual training
    trainset = loaded_data.build_full_trainset() #X-train
    model.fit(trainset)
    accuracy = get_model_accuracy(trainset = trainset, model = model)
    acc_label = int(accuracy*100)
    model_name = f'{acc_label}'
    export_model(model, model_name, model_type = 'surprise', model_extension ='pkl' )


def export_model(model, model_name = 'model', model_type = 'surprise', model_extension ='pkl', verbose = True) :
    with tempfile.NamedTemporaryFile(mode='rb+') as temp_file:
        pickle.dump({'model': model}, temp_file)
        path = f'machine_learning/models/{model_type}/{model_name}.{model_extension}'
        path_latest = f'machine_learning/models/{model_type}/latest.{model_extension}'
        if verbose:
            print(f'exporting to {path} and {path_latest}')
        storages.save(fpath=path, file_obj=File(temp_file), overwrite=False)
        storages.save(fpath=path_latest, file_obj=File(temp_file), overwrite=True)
  

def load_model( model_type = 'surprise', model_extension ='pkl'):
    path_latest = settings.MEDIA_ROOT / f"machine_learning/models/{model_type}/latest.{model_extension}"
    print(path_latest)
    model=None
    if path_latest.exists():
        with open(path_latest, 'rb') as f:
            model_data_loaded = pickle.load(f)
            model = model_data_loaded.get('model')
    else:
        raise ValueError("No model found.")
    return model
    
