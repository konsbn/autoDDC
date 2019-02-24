import json
import mechanicalsoup
from scraper import scrapertools
from itertools import chain
from collections import OrderedDict


class ISBNError(Exception):
    '''
    Raises an exception when ISBN is invalid
    '''

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


getter = scrapertools()


def ddc(isbn):
    '''
    Gets the Dewey Decimal Classification given isbn
    Input
    >>> isbn
    Output
    DDC
    '''
    url = "http://classify.oclc.org"
    url1 = url + "/classify2/ClassifyDemo?search-standnum-txt=" + \
        str(isbn) + "&startRec=0"
    getter.page_getter(url1)
    try:
        cat = getter.table_getter('classSummaryData')
    # if cat is not None:
    #     return cat
    # else:
    #     links = getter.table_getter('results-table')
    except AttributeError:
        links = getter.table_getter('results-table')
        return links


def isValid(isbn):
    '''
    Returns : True is Valid ISBN else False
    Eg:
    >>> isValid(9780231175968)
    True
    >>> isValid(123)
    Traceback (most recent call last):
        ...
    ISBNError: ('123', 'ISBN is Invalid')
    '''

    isbn = list(str(isbn))  # We need to iterate over this!
    if len(isbn) == 13:
        isbn = [int(j)*1 if (int(i)+1) % 2 != 0 else int(j)
                * 3 for i, j in enumerate(isbn)]
        if sum(isbn) % 10 == 0:
            return
        else:
            raise ISBNError(''.join(isbn), 'ISBN is Invalid')
    else:
        raise ISBNError(''.join(isbn), 'ISBN is Invalid')


def _categorylist(ddc):
    '''Just Gets The Broad classes upto the tenth place given broad DDC Class
       eg:

       DDC 500 will fetch everything till 599'''

    # Goes to the Summary Page of OCLC
    browser.open('https://www.oclc.org/en/dewey/features/summaries.html')
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


def make_ddc_db(path='./'):
    '''
    Gets the DDC_Categories if not found in the path and stores it for easy access
    '''
