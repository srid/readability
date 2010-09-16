from os import path
from glob import glob
import difflib

from readability import readable


def test_fixtures():
    fixtures_dir = path.join(path.dirname(__file__), 'fixtures')
    for urlf in glob(path.join(fixtures_dir, '*.url')):
        htmlf = urlf[:-4] + '.html'
        url = open(urlf).read().strip()
        print('url=%s' % url)
        
        expected_html = open(htmlf).read()
        actual_html = readable(url)
        diff = list(difflib.context_diff(
            actual_html.splitlines(), expected_html.splitlines()))
        assert not diff, '\n'.join(diff)
        