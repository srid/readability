# From http://github.com/scyclops/Readable-Feeds/blob/master/readability/hn.py
#    Originally written by Nirmal Patel (http://nirmalpatel.com/)
# License: GPL3

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

from BeautifulSoup import BeautifulSoup


NEGATIVE    = re.compile("comment|meta|footer|footnote|foot")
POSITIVE    = re.compile("post|hentry|entry|content|text|body|article")
PUNCTUATION = re.compile("""[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]""")


def grabContent(link, html):
    """Return (TITLE, CONTENT)
    
    where CONTENT is the readable version of ``html``
    """
    # Replace all doubled-up <BR> tags with <P> tags, and (TODO) remove fonts.
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

    # Study all the paragraphs and find the chunk that has the best score.
    # A score is determined by things like: Number of <p>'s, commas, special classes, etc.
    parents = []
    for paragraph in allParagraphs:

        parent = paragraph.parent

        if parent not in parents:
            parents.append(parent)
            parent.score = 0

            # Look for a special classname
            if "class" in parent:
                if NEGATIVE.match(parent["class"]):
                    parent.score -= 50
                if POSITIVE.match(parent["class"]):
                    parent.score += 25

            # Look for a special ID
            if "id" in parent:
                if NEGATIVE.match(parent["id"]):
                    parent.score -= 50
                if POSITIVE.match(parent["id"]):
                    parent.score += 25

        if parent.score is None:
            parent.score = 0

        # Add a point for the paragraph found
        innerText = paragraph.renderContents(
            )  # "".join(paragraph.findAll(text=True))
        if len(innerText) > 10:
            parent.score += 1

        # Add points for any commas within this paragraph
        parent.score += innerText.count(",")

    # Assignment from index for performance. See http://www.peachpit.com/articles/article.aspx?p=31567&seqNum=5 
    for parent in parents:
        if (not topParent) or (parent.score > topParent.score):
            topParent = parent

    if not topParent:
        return u""

    # REMOVES ALL STYLESHEETS ...
    styleLinks = soup.findAll("link", attrs={"type": "text/css"})
    for s in styleLinks:
        s.extract()

    # Remove all style tags in head
    for s in soup.findAll("style"):
        s.extract()

    # CLEAN STYLES FROM ELEMENTS IN TOP PARENT
    for ele in topParent.findAll(True):
        del ele['style']
        del ele['class']

    _killDivs(topParent)
    _clean(topParent, "form")
    _clean(topParent, "object")
    _clean(topParent, "iframe")

    _fixLinks(topParent, link)
    
    title = soup.find('title').text
    content = topParent.renderContents().decode('utf-8')

    return title, content


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
        # If the text content isn't laden with words, remove the child
        if t.renderContents().count(" ") < minWords:
            t.extract()


def _killDivs(parent):
    divs = parent.findAll("div")
    
    # Gather counts for other typical elements embedded within.
    # Traverse backwards so we can remove nodes at the same time without
    # effectiving the traversal.
    for d in divs:
        p     = len(d.findAll("p"))
        img   = len(d.findAll("img"))
        li    = len(d.findAll("li"))
        a     = len(d.findAll("a"))
        embed = len(d.findAll("embed"))
        pre   = len(d.findAll("pre"))
        code  = len(d.findAll("code"))

        # If the number of commas is less than 10 (bad sign) ...
        if d.renderContents().count(",") < 10:
            # DEVIATION: XXX: why do this?
            if (pre == 0) and (code == 0):
                # Add the number of non-paragraph elements is more than
                # paragraphs or other ominous signs
                if (img > p) or (li > p) or (a > p) or (p == 0) or (embed > 0):
                    d.extract()


def main():
    import webbrowser
    from tempfile import mkstemp
    from optparse import OptionParser
    
    usage = "usage: %prog [options] URL1 URL2 ..."
    parser = OptionParser(usage=usage)
    parser.add_option("-b", "--open-browser",
                  action="store_true", dest="open_browser", default=False,
                  help="show the readable version in a web browser")
    (options, args) = parser.parse_args()
    
    if not args:
        print(parser.format_help())
        sys.exit(2)
    
    for url in args:
        html = urllib.urlopen(url).read()
        title, content = grabContent(url, html)
        readable_html = r'''
<title>{title}</title>
<h1>{title}</h1>
{content}'''.format(title=title, content=content)
        if options.open_browser:
            fd, fn = mkstemp('readability.html')
            os.close(fd)
            with open(fn, 'w') as f:
                f.write(readable_html)
            webbrowser.open('file://' + os.path.abspath(fn))
        else:
            print(readable_html)


if __name__ == '__main__':
    main()
