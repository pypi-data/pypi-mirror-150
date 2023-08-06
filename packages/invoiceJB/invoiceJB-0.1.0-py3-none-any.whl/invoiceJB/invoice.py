import requests

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def get_current():
    ret = {}
    content = requests.get('https://invoice.etax.nat.gov.tw/invoice.xml')
    tree = ET.fromstring(content.text)
    items = list(tree.iter(tag='item'))
    title = items[0][0].text
    ret['title'] = title
    ptext = items[0][3].text
    ptext = ptext.replace('<p>', '')
    plist = ptext.split('</p>')

    for i in range(len(plist) - 1):
        tlist = plist[i].split('：')
        ret[tlist[0]] = tlist[1]

    return ret