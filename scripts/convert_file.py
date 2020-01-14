from bs4 import BeautifulSoup
from lxml import etree
from greek_normalisation.utils import nfc
import betacode.conv as conv

#XMLFILE = "Septuaginta (0527) - Bel et Draco (LXX) (058).xml"
XMLFILE = "Xenophon (0032) - Anabasis (006).xml"
raw = None
with open(XMLFILE, 'r', encoding='UTF-8') as f:
	raw = f.read()

xml = etree.fromstring(raw)

sentences = xml.xpath('//sentence')

print(len(sentences))

wcount = 0

for sent in sentences[0:2]:
	loc = sent.attrib['location']
	address = f"{0.}{sent.attrib['id']}" if loc.strip() == '' else f"{loc}.{sent.attrib['id']}"
	words = sent.xpath('./word')
	for w in words:
		wcount += 1
		wdict = w.attrib
		form = conv.beta_to_uni(wdict['form'])


		lemma = w.find('lemma')
		pos = lemma.attrib['POS'] if 'POS' in lemma.attrib else 'POS'
		entry = lemma.attrib['entry'] if 'entry' in lemma.attrib else 'LEMMA'
		print(f"{wcount} {form} {nfc(form)} {pos} POS {entry} {address}.{wdict['id']}")
