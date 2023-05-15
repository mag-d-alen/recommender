from platform import release
from faker import Faker
from  django.contrib.auth.hashers import make_password
import csv 
from django.conf import settings
from pprint import pprint
import datetime

MOVIE_METADATA_CSV = settings.DATA_DIR / "movies_metadata.csv"


def get_fake_profiles(count=10):
    fake =Faker()
    user_data = []
    for _ in range(count): 
        profile = fake.profile()   
        if "name" in profile:
            f_name, l_name = profile.get("name").split(" ")[:2] 
        data = {
            "username": profile.get("username"),
            "email":  f"{f_name}.{l_name}@{fake.domain_name()}",
            "is_active": True,
            "password": "make_password(fake.password(length=15)"
        }
        data["first_name"] = f_name
        data["last_name"] = l_name
        user_data.append(data)
    return user_data
    
           
           
def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except:
        return None
    return date_str

def load_movie_data(limit=10):
    with open(MOVIE_METADATA_CSV, newline = '', encoding="utf8")  as csvfile:
       reader= csv.DictReader(csvfile)
       dataset = []
       for i, row in enumerate(reader):
            _id = row.get('id')
            try:
               _id = int(_id)
            except:
                _id = None
            release_date = validate_date(row.get('release_date'))
            data = {
                "id": _id,
                "title": row.get('title'),
                "overview": row.get('overview'),
                "release_date": release_date,
            }
            dataset.append(data)
            if i + 1 > limit:
               break
    return dataset

                            
                                   