# From http://github.com/scyclops/Readable-Feeds/blob/master/readability/hn.py
#    This file originally written by Nirmal Patel (http://nirmalpatel.com/).
# License: GPL

import os
import sys
import urllib
import urlparse
import re
import HTMLParser
import rfc822
from datetime import datetime
from pickle import dumps, loads
import time

import feedparser
from BeautifulSoup import BeautifulSoup


NEGATIVE    = re.compile("comment|meta|footer|footnote|foot")
POSITIVE    = re.compile("post|hentry|entry|content|text|body|article")
PUNCTUATION = re.compile("""[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]""")


def grabContent(link, html):
    replaceBrs = re.compile("<br */? *>[ \r\n]*<br */? *>")
    html = re.sub(replaceBrs, "</p><p>", html)

    try:
        soup = BeautifulSoup(html)
    except HTMLParser.HTMLParseError:
        return u""

    # REMOVE SCRIPTS
    for s in soup.findAll("script"):
        s.extract()

    allParagraphs = soup.findAll("p")
    topParent = None

    parents = []
    for paragraph in allParagraphs:

        parent = paragraph.parent

        if (parent not in parents):
            parents.append(parent)
            parent.score = 0

            if ("class" in parent):
                if (NEGATIVE.match(parent["class"])):
                    parent.score -= 50
                if (POSITIVE.match(parent["class"])):
                    parent.score += 25

            if ("id" in parent):
                if (NEGATIVE.match(parent["id"])):
                    parent.score -= 50
                if (POSITIVE.match(parent["id"])):
                    parent.score += 25

        if (parent.score == None):
            parent.score = 0

        innerText = paragraph.renderContents(
            )  # "".join(paragraph.findAll(text=True))
        if (len(innerText) > 10):
            parent.score += 1

        parent.score += innerText.count(",")

    for parent in parents:
        if ((not topParent) or (parent.score > topParent.score)):
            topParent = parent

    if (not topParent):
        return u""

    # REMOVE LINK'D STYLES
    styleLinks = soup.findAll("link", attrs={"type": "text/css"})
    for s in styleLinks:
        s.extract()

    # REMOVE ON PAGE STYLES
    for s in soup.findAll("style"):
        s.extract()

    # CLEAN STYLES FROM ELEMENTS IN TOP PARENT
    for ele in topParent.findAll(True):
        del(ele['style'])
        del(ele['class'])

    _killDivs(topParent)
    _clean(topParent, "form")
    _clean(topParent, "object")
    _clean(topParent, "iframe")

    _fixLinks(topParent, link)

    return topParent.renderContents().decode('utf-8')


def _fixLinks(parent, link):
    tags = parent.findAll(True)

    for t in tags:
        if "href" in t:
            t["href"] = urlparse.urljoin(link, t["href"])
        if "src" in t:
            t["src"] = urlparse.urljoin(link, t["src"])


def _clean(top, tag, minWords=10000):
    tags = top.findAll(tag)

    for t in tags:
        if (t.renderContents().count(" ") < minWords):
            t.extract()


def _killDivs(parent):
    divs = parent.findAll("div")
    for d in divs:
        p     = len(d.findAll("p"))
        img   = len(d.findAll("img"))
        li    = len(d.findAll("li"))
        a     = len(d.findAll("a"))
        embed = len(d.findAll("embed"))
        pre   = len(d.findAll("pre"))
        code  = len(d.findAll("code"))

        if (d.renderContents().count(",") < 10):
            if ((pre == 0) and (code == 0)):
                if (img > p) or (li > p) or (a > p) or (p == 0) or (embed > 0):
                    d.extract()


def main():
    url = sys.argv[1]
    data = urllib.urlopen(url).read()
    print grabContent(url, data)


if __name__ == '__main__':
    main()
