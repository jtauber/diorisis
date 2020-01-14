#!/usr/bin/env python3

import glob

from lxml import etree

print(
    "author",
    "title",
    "tlgAuthor",
    "tlgId",
    "lang",
    "date",
    "genre",
    "subgenre",
    sep="\t",
)

for filename in sorted(glob.glob("raw-data/Diorisis/*.xml")):
    with open(filename) as f:
        tree = etree.parse(f)

        titleStmt = tree.xpath("/TEI.2/teiHeader/fileDesc/titleStmt")[0]
        profileDesc = tree.xpath("/TEI.2/teiHeader/profileDesc")[0]
        xenoData = tree.xpath("/TEI.2/teiHeader/xenoData")[0]

        title = titleStmt.xpath("title")[0].text
        author = titleStmt.xpath("author")[0].text
        tlgAuthor = titleStmt.xpath("tlgAuthor")[0].text
        tlgId = titleStmt.xpath("tlgId")[0].text

        language = profileDesc.xpath("langUsage/language")[0]
        language_text = language.text
        language_ident = language.attrib["ident"]
        creation_date = profileDesc.xpath("creation/date")[0].text

        genre = xenoData.xpath("genre")[0].text
        subgenre = xenoData.xpath("subgenre")[0].text

        print(
            author,
            title,
            tlgAuthor,
            tlgId,
            language_ident,
            creation_date,
            genre,
            subgenre,
            sep="\t",
        )
