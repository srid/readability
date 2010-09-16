import os
from os import path
from glob import glob
import difflib
import tempfile

from readability import readable


def test_fixtures():
    def test_fixture(url, expected_html):
        print('url=%s' % url)
        
        actual_html = readable(url)
        
        # Write the HTML for late diagnosis
        _, actual_html_fn = tempfile.mkstemp('readabilitytest')
        os.close(_)
        _, expected_html_fn = tempfile.mkstemp('readabilitytest')
        os.close(_)
        with open(actual_html_fn, 'w') as f:
            f.write(actual_html)
        with open(expected_html_fn, 'w') as f:
            f.write(expected_html)
        
        diff = list(difflib.context_diff(
            actual_html.splitlines(), expected_html.splitlines()))
        diff_string = '\n'.join(diff)
        assert not diff, (
            'readable version differs; diff:\n{0}\n'
            'expected: {1}\n'
            'actual: {2}').format(
            diff_string,
            expected_html_fn,
            actual_html_fn,
        )
        
    fixtures_dir = path.join(path.dirname(__file__), 'fixtures')
    for urlf in glob(path.join(fixtures_dir, '*.url')):
        url = open(urlf).read().strip()
        htmlf = urlf[:-4] + '.html'
        expected_html = open(htmlf).read()
        
        yield path.basename(urlf), test_fixture, url, expected_html