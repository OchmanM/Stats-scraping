import requests
import logging
from lxml import etree
import time
from ..models import *
from ..celery_functions import meta_functions
from ..celery_functions import db_functions

logging.basicConfig(filename='webscrap.log',
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

waiting_time = 4
# Returns list of online players from onlineURL
# Returns list
def get_online():
    parser = etree.HTMLParser()
    # URL
    online_url = "http://classictibia.com/onlinelist.php"
    page_content = requests.get(online_url)
    tree = etree.fromstring(page_content.text, parser=parser)

    # Get only names
    names = tree.xpath('//*[@class="special"]/td[2]/a/text()')
    logging.info("[GET ONLINE] Collected names %s" % (names))
    time.sleep(waiting_time)

    return names


# Get's character information from characterprofile.php?name=
# Returns dict key:value, where key is model's field name at the same time.
def get_player_info(name, parse_deathlist=False):
    parser = etree.HTMLParser()
    # URL

    logging.debug("Collecting info for name %s" % (name))
    online_url = "http://classictibia.com/characterprofile.php?name=" + name
    page_content = requests.get(online_url, headers={'User-Agent':'ClassicStats'})
    tree = etree.fromstring(page_content.text, parser=parser)
    # Get only names
    player_info = []

    for i in range(1, 9):
        scrap_value = meta_functions.get_field_value(tree, i)
        if scrap_value:
            player_info.insert(len(player_info), scrap_value)

    player_info_fixed = {}
    try:
        # Make informations dictionary
        player_info_fixed = {each[0]: each[1] for each in player_info if each is not None}
        player_info_fixed.update({'lastlogin': meta_functions.normalize_datetime(player_info_fixed['lastlogin'])})
        logging.debug("Fixed info % s" % player_info_fixed)
        if parse_deathlist:
            get_death_list(name, tree)
    except:
        logging.info("Couldn't find info for player %s" % name)
    time.sleep(waiting_time)

    return player_info_fixed


# From tree, parse and find deathlist
# Void
def get_death_list(name, tree=None):
    # URL
    logging.debug("Collecting deaths for name %s" % (name))
    if tree is None:
        parser = etree.HTMLParser()
        online_url = "http://classictibia.com/characterprofile.php?name=" + name
        page_content = requests.get(online_url)
        tree = etree.fromstring(page_content.text, parser=parser)
        time.sleep(waiting_time)

    xpath = './/*[@id="content"]/li//text()'
    deaths_text = tree.xpath(xpath)
    deaths_info = {}

    if deaths_text:
        # Normalize deaths
        deaths_text = [death.replace('\n\t\t\t\t\t\t\t\t\t', '') for death in deaths_text]
        logging.debug("[GET DEATHLIST] Deaths %s" % (deaths_text))

        for i, each in enumerate(deaths_text):
            if each[0] != '[':
                continue
            is_pvp_death = meta_functions.deathlist_is_pvp(each)
            if is_pvp_death:
                if not db_functions.get_player_id(deaths_text[i + 1]):
                    db_functions.create_player(deaths_text[i + 1])
                try:
                    killer = Player.objects.get(name=deaths_text[i + 1])
                except Player.DoesNotExist:
                    killer = None
            else:
                killer = None

            try:
                killed = Player.objects.get(name=name)
            except Player.DoesNotExist:
                db_functions.create_player(name)
                killed = Player.objects.get(name=name)

            if killer is not None:
                text = each + deaths_text[i + 1]
            else:
                text = each

            date = meta_functions.normalize_datetime(meta_functions.deathlist_get_date(each))
            level = int(meta_functions.deathlist_get_level(each))
            deaths_info = {}
            deaths_info.update(
                {'killed': killed,
                 'killer': killer,
                 'date': date,
                 'pvp': is_pvp_death,
                 'text': text,
                 'level': level}
            )
            logging.info("[GET DEATHLIST] Collected deaths %s" % deaths_info)

            try:
                Deaths.objects.update_or_create(killer=deaths_info['killer'],
                                                date=deaths_info['date'],
                                                killed=deaths_info['killed'],
                                                text=deaths_info['text'],
                                                level=deaths_info['level'],
                                                defaults={**deaths_info}
                                                )
            except:
                logging.critical("[GET DEATHLIST] Couldn't collect deaths")