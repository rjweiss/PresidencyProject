__author__ = 'Rebecca'

import re
import pymongo
from lxml.html import parse

def scrape():
    mongo = pymongo.Connection('localhost', 27017)
    db = mongo.platforms
    site = parse('http://www.presidency.ucsb.edu/platforms.php')
    root = site.getroot()
    elements = root.xpath('//td[@class="doctext"]//a')
    links = [element.attrib['href'] for element in elements]

    urls = []
    for link in links:
        if not link.endswith('.pdf'):
            urls.append(link)

    pages = []
    for url in urls:
        page = parse(url)
        pages.append(page)

    for page in pages:
        YEAR_PATTERN = re.compile('\d{4}')
        root = page.getroot()
        title = root.xpath('//title')[0].text
        displaytext = root.xpath('//span[@class="displaytext"]//p')
        text = []
        party = str()
        for p in displaytext:
            text.append(unicode(p.text))
        text = [unicode(paragraph.strip()) for paragraph in text]
        if re.search('Democratic', title):
            party = 'Democrat'
        if re.search('Republican', title):
            party = 'Republican'
        flat_text = " ".join(text)
        try:
            year = YEAR_PATTERN.findall(title)[0]
        except:
            year = 'null'
        document = {'year': year, 'party': party, 'text': flat_text}
        db.platforms.insert(document)

def main():
    scrape()
    print 'Done.'

if __name__ == '__main__':
    main()