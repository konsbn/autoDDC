import mechanicalsoup


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
        self.browser.open(url)
        self.page = self.browser.get_current_page()

    def table_getter(self, ids):
        '''
        Gets the tables based on id from the current page.
        '''
        return self.page.find('table', {'id': ids}).find('tbody')
