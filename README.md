# Recommender

Build a recommendation engine using Django &amp; a Machine Learning technique called Collaborative Filtering.

## Getting Started

1. Clone the project and make it your own. Use branch `start` initially so we can all start in the same place.

```bash
git clone https://github.com/codingforentrepreneurs/recommender
cd recommender
git checkout start
rm -rf .git
git init .
git add --all
git commit -m "My recommender project"
```

2. Create virtual environment and activate it.

```bash
python3.8 -m venv venv
source venv/bin/activate
```

Use `.\venv\Scripts\activate` if on windows

3. Install requirements

```
(venv) python -m pip install pip --upgrade
(venv) python -m pip install -r requirements.txt
```

4. Open VSCode

```bash
code .
```

5. Get to work.

## Helpful Guides

- [Using a Cloud-based Redis Server](https://www.codingforentrepreneurs.com/blog/remote-redis-servers-for-development/)
- [Install Redis on Windows](https://www.codingforentrepreneurs.com/blog/redis-on-windows/)
- [Install Redis on macOS](https://www.codingforentrepreneurs.com/blog/install-redis-mac-and-linux)
- [Celery + Redis + Django Setup Guide](https://www.codingforentrepreneurs.com/blog/celery-redis-django/)

6. to run celery on windows:

   to start on windows- two venv terminals in src:
   celery -A home worker -l info -P gevent
   celery -A home beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   start redis server
   and python manage.py runserver

7. to run jupyter : cd src //python manage.py shell_plus --notebook
8. to add new dependencies python -m pip install -r ../requirements.txt
 