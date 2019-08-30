import json
import os
import mechanicalsoup
from scraper import scrapertools
from itertools import chain
from collections import OrderedDict

browser = mechanicalsoup.StatefulBrowser()


def _categorylist(ddc):
    '''Just Gets The Broad classes upto the tenth place given broad DDC Class
       eg:

       DDC 500 will fetch everything till 599'''

    # Goes to the Summary Page of OCLC
    browser.open('https://www.oclc.org/en/dewey/resources/summaries.html')
    page = browser.get_current_page()
    cat = page.find('a', {'name': str(ddc)}).find_next(
        'tr').contents  # Finds the Table of DDC and writes it to cat
    while '\n' in cat:  # Basic Cleanup
        cat.remove('\n')
    cat = [i.string for i in (
        cat[0].contents + cat[1].contents) if i.string is not None]
    return(cat)


def GetAllCategory():
    '''
    Gets all the DDC Categories from 000 to 999
    Output : OrderedDict[DDC] = 'Genre'
    '''
    DDC_Categories = ['000', '100', '200', '300',
                      '400', '500', '600', '700', '800', '900']
    # Fetch DDC Genres For all the Broad Categories and Chain
    # together in one list. String cleanup is performed to strip
    # whitespaces. Should have done it more explicitly
    CatList = [i.strip() for i in list(chain.from_iterable(
        map(_categorylist, DDC_Categories))) if i != ' ']
    # CatList -> Complete_DDC_Categories[DDC] = Genre
    Complete_DDC_Categories = OrderedDict()
    for i in CatList:
        ddc_class, genre = i.split(' ')[0], ' '.join(i.split(' ')[1:])
        Complete_DDC_Categories.update(OrderedDict([(ddc_class, genre)]))
    return(Complete_DDC_Categories)


def store_categories(filename='ddc_summary.json'):
    with open(filename, 'w') as outfile:
        json.dump(GetAllCategory(), outfile)


def read_categories(filename='ddc_summary.json'):
    return json.load(open('ddc_summary.json'), object_pairs_hook=OrderedDict)


def check_if_exists(path='./'):
    return os.path.isfile(path+'ddc_summary.json')


def get_summaries():
    if check_if_exists():
        return read_categories()
    else:
        store_categories()
        return read_categories()
