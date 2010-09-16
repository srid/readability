from os import path
from glob import glob
import difflib

from readability import readable


def test_fixtures():
    def test_fixture(url, expected_html):
        print('url=%s' % url)
        
        actual_html = readable(url)
        diff = list(difflib.context_diff(
            actual_html.splitlines(), expected_html.splitlines()))
        assert not diff, '\n'.join(diff)
        
    fixtures_dir = path.join(path.dirname(__file__), 'fixtures')
    for urlf in glob(path.join(fixtures_dir, '*.url')):
        url = open(urlf).read().strip()
        htmlf = urlf[:-4] + '.html'
        expected_html = open(htmlf).read()
        
        yield path.basename(urlf), test_fixture, url, expected_html