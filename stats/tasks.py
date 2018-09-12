import logging
from .models import *
from celery import Celery
from mysite.celery import app
from .celery_functions import db_functions
from .celery_functions import webscrap_functions
import time

celery = Celery('tasks',
                broker='amqp://guest@localhost//')


logging.basicConfig(filename='tasks.log',
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


@app.task()
def update_all_characters():
    all_players = Player.objects.all()
    for each in all_players:
        while (db_functions.get_celery_blocker() == True):
            time.sleep(5)
        db_functions.create_player(each.name, webscrap_functions.get_player_info(each.name, True))


@app.task()
def collect_online():
    db_functions.switch_celery_in_use(False,True)
    time.sleep(5)

    online_by_database = db_functions.get_online_by_database()
    online_by_webpage = webscrap_functions.get_online()

    for each in online_by_database:
        if each not in online_by_webpage:
            db_functions.update_offline(each)

    for each in online_by_webpage:
        if db_functions.get_player_id(each) is None:
            db_functions.create_player(each, webscrap_functions.get_player_info(each, True))
        if each not in online_by_database:
            db_functions.update_online(each)

    for each in online_by_database:
        if each not in online_by_webpage:
            db_functions.create_player(each, webscrap_functions.get_player_info(each, True))

    db_functions.switch_celery_in_use(True, False)


@app.on_after_configure.connect
def add_periodic(**kwargs):
    app.add_periodic_task(60.0, collect_online.s(), name='CollectOnline_every_min')
    app.add_periodic_task(360.0, update_all_characters.s(), name='UpdateAllCharacters_every_6_min')
