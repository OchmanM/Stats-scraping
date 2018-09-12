import logging
import re
from datetime import datetime

logging.basicConfig(filename='meta.log',
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


# Get's field: value from given character link /characterprofile.php?name= where tree is html code and i is table column index.
# Returns table, where index 0 = field, index 1 = value
def get_field_value(tree, i):
    xpath = '//*[@id="content"]/table/tbody/tr['
    xpath += str(i)
    xpath += ']/td//text()'

    scraped_text = tree.xpath(xpath)

    # Given ['field', 'value'], cleans 'field' from spaces and ":"
    if scraped_text:
        scraped_text[0] = scraped_text[0].replace(':', '').replace(' ', '').replace('\t', '').lower()
        if scraped_text[0] == 'guild':
            try:
                del scraped_text[1]
                del scraped_text[2]
            except:
                del scraped_text[:]

    logging.info("Collected information %s" % (scraped_text))
    return scraped_text


# Normalizes date format 03 June 2018 (17:37)
# Returns datetime
def normalize_datetime(dateString):
    return datetime.strptime(dateString,'%d %B %Y (%H:%M)')



# Gets data from format:
# [01 August 2018 (20:55)] Killed at level 103 by player: Nickname

# Given deathlist text, parses it to return Date
# Returns date in string format
def deathlist_get_date(text):
    result = re.search(r'\[(.*?)\]', text)
    return result.group(1) if result else None


# Given deathlist text, parses it to return level
# Returns string
def deathlist_get_level(text):
    result = re.search(r'level (\d*) ', text)
    return result.group(1) if result else None

# Given deathlist text, parses it to check if death was due to PvP
# Returns True / False (bool)
def deathlist_is_pvp(text):
    result = re.search(r'by player?(.*)', text)
    return True if result else False
