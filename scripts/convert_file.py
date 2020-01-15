#from bs4 import BeautifulSoup
from lxml import etree
from greek_normalisation.utils import nfc
import betacode.conv as conv
import glob
#XMLFILE = "./raw-data/Septuaginta (0527) - Bel et Draco (LXX) (058).xml"
#XMLFILE = "./raw-data/Xenophon (0032) - Anabasis (006).xml"

# add sents, and chapters etc.

wcount = 0
sentence_count = 0
book_count = 0
s_list = []
books = []
chapters = []
book_start = 0
book_end = 0
cpt_start = 0
book_name_numbers = []
CORPUS_PREFIX = "lxx"
with open(CORPUS_PREFIX + "_tokens.txt", 'w', encoding = "UTF-8") as tokens:

    for filename in sorted(glob.glob("../raw-data/Septuaginta (0527)*.xml")):
        print(filename)
        book_count += 1
        book_name_numbers.append(f"{book_count:02d} {filename.replace('../raw-data/', '')}")
        book_start = book_end + 1
        with open(filename, 'r', encoding='UTF-8') as f:
            sentence_count = 0
            chapter_count = 0
            raw = f.read()
            xml = etree.fromstring(raw)
            sentences = xml.xpath('//sentence')
            last_loc = -1
            cpt_start = wcount + 1
            for sent in sentences:
                sent_start = wcount + 1
                sentence_count +=1
                # need this line because some Psalms locations have text as well as numbers
                loc_raw = sent.attrib['location'].split(' ', maxsplit=1)[0]
                if loc_raw == 'Prologus': #Syracides has this
                    loc = 0
                else:
                    loc = int(loc_raw) if not loc_raw.strip() == '' else 0
                if loc != last_loc:
                    chapters.append(f"{book_count:02d}{last_loc:02d} {cpt_start} {wcount}")
                    last_loc = loc
                    cpt_start = wcount + 1
                #address = f"{0.}{sent.attrib['id']}" if loc.strip() == '' else f"{loc}.{sent.attrib['id']}"
                words = sent.xpath('./word')
                for w in words:
                    wcount += 1
                    wdict = w.attrib
                    form = conv.beta_to_uni(wdict['form'])
                    lemma = w.find('lemma')
                    pos = lemma.attrib['POS'] if 'POS' in lemma.attrib else 'POS'
                    entry = lemma.attrib['entry'] if 'entry' in lemma.attrib else 'LEMMA'
                    print(f"{wcount} {form} {nfc(form)}   {entry}", file=tokens)
                s_list.append(f"{book_count:02d}{loc:02d}{sentence_count:02d} {sent_start} {wcount}")

            book_end = wcount
            books.append(f"{book_count:02d} {book_start} {book_end}")



def output_data(fname, data):
    with open(fname, 'w', encoding="UTF-8") as f:
        for d in data:
            f.write(d + "\n")

output_data(CORPUS_PREFIX + "_books.txt", books)

output_data(CORPUS_PREFIX + "_sentences.txt", s_list)
output_data(CORPUS_PREFIX + "_chatpers.txt", chapters)

output_data(CORPUS_PREFIX + '_books_map.txt', book_name_numbers)
