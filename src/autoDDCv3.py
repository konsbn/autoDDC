import categories as cat
import mechanicalsoup
from scraper import scrapertools
from isbntools.app import meta
from collections import OrderedDict
from titleauthor import get_title_author


class ISBNError(Exception):
    '''
    Raises an exception when ISBN is invalid
    '''

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def isddc(ddc):
    try:
        float(ddc)
        return True
    except ValueError:
        return False


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


class AutoDDC:
    def __init__(self):
        '''
        Initializes the Browser Class
        '''
        self.browser = mechanicalsoup.StatefulBrowser()
        self.getter = scrapertools()
        self.summaries = cat.get_summaries()

    def find_in_url(self, url):
        '''
        Finds the DDC in the current page or returns the list of links to follow
        '''
        self.getter.page_getter(url)
        try:
            self.cat = self.getter.table_getter('classSummaryData')
            # if self.cat is not None:
            return self.cat
        except AttributeError:
            self.links = self.getter.table_getter('results-table')
            return self.links

    def ddc_urlwrapper(self, isbn):
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
        return url1

    def pretty_ddc(self):
        try:
            for i in self.cat.values():
                if i['DDC:'] == 'Most Frequent':
                    if isddc(i['Class Number']):
                        return i['Class Number']
        except AttributeError:

            self.find_in_url(self.links[0]['Link'])
            for i in self.cat.values():
                if i['DDC:'] == 'Most Frequent':
                    if isddc(i['Class Number']):
                        return i['Class Number']


def wrapper(isbn, genre=True):
    try:
        ddc_scraper = AutoDDC()
        ddc_scraper.find_in_url(ddc_scraper.ddc_urlwrapper(isbn))
        ddc = ddc_scraper.pretty_ddc()
        current_page = ddc_scraper.getter.page

        if genre:
            genre = ddc_scraper.summaries[str(int(float(ddc)))]
            try:
                metadata = meta(str(isbn))
                title, author = metadata['Title'], metadata['Authors'][0]
            except:
                metadata = get_title_author(current_page)
                title, author = metadata

            return OrderedDict([('DDC', ddc), ('Title', title), ('Author', author),  ('Genre', genre)])
        return ddc
    except ConnectionError:
        return('Internet Not Connected')
    except AttributeError:
        return(f'No Entry for {isbn}')
