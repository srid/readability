import sys
import os
from os import path
from fabric.api import *
# Import github.com/srid/fablib
sys.path.append(path.abspath(
    path.join(path.dirname(__file__), 'fablib')))
import venv

clean = venv.clean
init = venv.init


def init(pyver='2.7', dir='.', upgrade=False, clientonly=False):
    """Create a virtualenv and setup entry points
    """
    virtualenv = venv.init(
        pyver=pyver,
        dir=dir,
        upgrade=upgrade,
        apy=True
    )
    
    # extra required packages
    extra = ['pytest']
    for p in extra:
        venv.install(p, dir)
        
        
def test():
    """Run unit/regression test suite"""
    if not path.exists('tmp'):
        os.makedirs('tmp')
    local('{0} -x -v test/test.py --junitxml=tmp/testreport.xml'.format(
        venv.get_script('py.test')
    ), capture=False)
    