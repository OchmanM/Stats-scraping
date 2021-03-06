import logging
from ..models import *
from datetime import datetime
from ..celery_functions import webscrap_functions

logging.basicConfig(filename='db.log',
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


# Creates or updates character - name is character name && info is dict field: value
# Returns nothing (void)
def create_player(name, info=None):
    if info is None:
        info = webscrap_functions.get_player_info(name)
    try:
        logging.info("[CREATE PLAYER] Update or create object %s" % info)
        Player.objects.update_or_create(name = info['name'], defaults ={**info})
    except Exception as e:
        logging.critical("[CREATE PLAYER]Couldn't update or create object %s " % info)
        logging.critical("[CREATE PLAYER] Error: %s " % e)


# Returns list of characters which have OnlineDetails logout empty
# Returns list of strings
def get_online_by_database():
    players = OnlineDetails.objects.filter(logout__isnull=True)
    names = []
    try:
        if players:
            names = [Player.objects.get(pk=each).name for each in players.values_list('player', flat=True)]
            logging.info("[GET ONLINE BY DB] Collected Names: % s" % names)

    except Exception as e:
        logging.critical("[LOGOUT CHARS] Error: %s " % e)

    return names


# Update_or_create based on get_player_info() from webpage
# Void

# [OBSOLETE]?
def update_player_info(player_name):
    player_info = webscrap_functions.get_player_info(player_name, True)
    create_player(player_name, player_info)
    try:
        player_update = {}
        player_update['player'] = Player.objects.get(name=player_name)
        player_update['level'] = player_info['level']
        if player_info['status'] == "OFFLINE":
            player_update['logout'] = datetime.now()
        logging.debug("[UPDATE ONLINE] Adding online details %s " % player_update)

        OnlineDetails.objects.update_or_create(login=player_info['lastlogin'], defaults = {**player_update})

    except Exception as e:
        logging.critical("[UPDATE PLAYER INFO] Couldn't update or create object %s " % player_name)
        logging.critical("[UPDATE PLAYER INFO] Error: %s " % e)


# Updates Offline date to OnlineDetails
# Void
def update_offline(player_name):
    try:
        is_online = OnlineDetails.objects.filter(logout__isnull=True, player=get_player_id(player_name)).update(logout = datetime.now())
        logging.info("[UPDATE_ONLINE] Setting %s to offline" % player_name)

    except OnlineDetails.DoesNotExist:
        logging.critical("[UPDATE OFFLINE] Person is offline already")


# Updates Online date to OnlineDetails
# Void
def update_online(player_name):
    if not OnlineDetails.objects.filter(logout__isnull=True, player=get_player_id(player_name)).exists():
        try:
            OnlineDetails.objects.create(player=Player.objects.get(name=player_name),
                                         login=datetime.now())
            logging.info("[UPDATE_ONLINE] Setting %s to online" % player_name)
        except Exception as e:
            logging.critical("[UPDATE_ONLINE] %s" %e)
    else:
        logging.info("[UPDATE_ONLINE] Somehow %s is online" % player_name)


# Given name, checks if character exists in "Player" model
# Returns ID or None
def get_player_id(playerName):
    try:
        exists = Player.objects.get(name=playerNameG)
    except Player.DoesNotExist:
        create_player(playerName)
        try:
            exists = Player.objects.get(name=playerName)
        except Player.DoesNotExist:
            exists = None
    return exists.id if exists else None


# Given name, checks if player is online in database
# Returns True or False
def is_online(playerName):
    try:
        get_online = OnlineDetails.objects.filter(
            logout__isnull=True,
            player=get_player_id(playerName)
            )
    except OnlineDetails.DoesNotExist:
        get_online = False
    return True if get_online else False


# Checks if CeleryInUse.is_in_use == True.
# Returns True or False
def get_celery_blocker():
    try:
        get_celery = CeleryInUse.objects.get(is_in_use=True)
        return True
    except CeleryInUse.DoesNotExist:
        return False


# Switches CeleryInUse.is_in_use from value_get to value_set
# Void
def switch_celery_in_use(value_get, value_set):
    try:
        get_celery = CeleryInUse.objects.get(is_in_use=value_get)
        get_celery.is_in_use = value_set
        get_celery.save(update_fields=['is_in_use'])

    except CeleryInUse.DoesNotExist:
        pass