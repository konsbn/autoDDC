from scraper import scrapertools


def get_title_author(page):
    '''
    Gets the title and author from the page from the item summary
    '''
    item_summary = page.find('div', {'id': 'display-Summary'})
    headers = [i.text for i in item_summary.find_all('dt')]
    entries = [i.text for i in item_summary.find_all('dd')]
    table = dict(zip(headers, entries))
    # author = ','.join(table['Author:'].split(',')[:-1])
    author = table['Author:']
    author = ' '.join(author.split(';')[0].split(',')[::-1][1:])
    title = table['Title:']
    return title, author
