__author__ = 'Rebecca'

import re
from lxml.html import parse
from lxml import etree

site = parse('http://www.presidency.ucsb.edu/platforms.php')
root = site.getroot()
elements = root.xpath('//td[@class="doctext"]//a')
links = [element.attrib['href'] for element in elements]

urls = []

for link in links:
    if not link.endswith('.pdf'):
        urls.append(link)

democrat_platforms = []
republican_platforms = []

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
    for p in displaytext:
        text.append(unicode(p.text))
    text = [unicode(paragraph.strip()) for paragraph in text]
    flat_text = " ".join(text)
    if re.search('Democratic', title):
        democrat_platforms.append((YEAR_PATTERN.findall(title), flat_text))
    if re.search('Republican', title):
        republican_platforms.append((YEAR_PATTERN.findall(title), flat_text))
