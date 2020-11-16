import mechanicalsoup
from collections import OrderedDict


class scrapertools:
    '''
    Provides a suite of tools for opening web pages
    with scraping and cleanup tools.
    '''

    def __init__(self):
        '''
        Initializes the scrapertools class with the browser instance
        '''
        self.browser = mechanicalsoup.StatefulBrowser()

    def page_getter(self, url):
        '''
        Returns the current page of the url to be opened
        '''
        self.base_url = '/'.join(url.split('/')[:-1])  # Gets the base url
        self.browser.open(url)
        self.page = self.browser.get_current_page()

    def _scraper(self, html):
        '''
        A cleanup utility for detagging html and checks for links
        '''
        if html.find('a', href=True) is not None:
            return html.contents[0].string, html.find('a', href=True)['href']
        return html.string

    def _table_cleaner(self, od):
        '''
        Performs the cleanup for the results table so it gives both the title
        and the link separately
        '''
        title, link = od['Title & Author']
        od.update(OrderedDict([('Title & Author', title)]))
        od.update(OrderedDict(
            [('Link', self.base_url + '/' + '/'.join(link.split('/')[2:]))]))
        return od

    def table_getter(self, ids):
        '''
        Gets the tables based on id from the current page.
        '''

        table = self.page.find('table', {'id': ids})  # Finds table by id
        head = table.find('thead')  # Finds the table head
        body = table.find('tbody')  # Finds the body of the table
        # Extracts the headers from table head
        headers = [tag.string for tag in head.find_all('th')]
        # Finds all the titles in the body
        body = [entry.find_all('td')for entry in body.find_all('tr')]
        # Removes Empty Elements
        if [] in body:
            body.remove([])
        body = [[self._scraper(j) for j in i] for i in body]
        body = [list(zip(headers, j)) for j in body]
        self.table = OrderedDict({i: OrderedDict(
            {j[0]: j[1] for j in body[i]})for i in range(len(body))})
        if ids == 'results-table':
            for i in self.table.keys():
                self._table_cleaner(self.table[i])
        return self.table
