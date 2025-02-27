# Copyright (c) 2008-2015 by Enthought, Inc.
# All rights reserved.
import os
import re
import subprocess

from setuptools import setup, find_packages

MAJOR = 4
MINOR = 7
MICRO = 0

IS_RELEASED = True

VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

# Name of the directory containing the package.
PKG_PATHNAME = 'envisage'

# Name of the file containing the version information.
_VERSION_FILENAME = os.path.join(PKG_PATHNAME, '_version.py')


def git_version():
    """ Parse version information from the current git commit.

    Parse the output of `git describe` and return the git hash and the number
    of commits since the last version tag.
    """

    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            env=env, ).communicate()[0]
        return str(out)

    try:
        # We ask git to find the latest tag matching a glob expression. The
        # intention is to find a release tag of the form '4.50.2'. Strictly
        # speaking, the glob expression also matches tags of the form
        # '4abc.5xyz.2gtluuu', but it's very difficult with glob expressions
        # to distinguish between the two cases, and the likelihood of a
        # problem is minimal.
        out = _minimal_ext_cmd(
            ['git', 'describe', '--match', '[0-9]*.[0-9]*.[0-9]*', '--tags'])
    except OSError:
        out = ''

    git_description = out.strip()#.decode('ascii')
    expr = r'.*?\-(?P<count>\d+)-g(?P<hash>[a-fA-F0-9]+)'
    match = re.match(expr, git_description)
    if match is None:
        git_revision, git_count = 'Unknown', '0'
    else:
        git_revision, git_count = match.group('hash'), match.group('count')

    return git_revision, git_count


def write_version_py(filename=_VERSION_FILENAME):
    """ Create a file containing the version information. """

    template = """\
# This file was automatically generated from the `setup.py` script.
version = '{version}'
full_version = '{full_version}'
git_revision = '{git_revision}'
is_released = {is_released}

if not is_released:
    version = full_version
"""
    # Adding the git rev number needs to be done inside
    # write_version_py(), otherwise the import of _version messes
    # up the build under Python 3.
    fullversion = VERSION
    if os.path.exists('.git'):
        git_rev, dev_num = git_version()
    elif os.path.exists(filename):
        # must be a source distribution, use existing version file
        try:
            from envisage._version import git_revision as git_rev
            from envisage._version import full_version as full_v
        except ImportError:
            msg = ("Unable to import 'git_revision' or 'full_revision'. "
                   "Try removing {} and the build directory before building.")
            raise ImportError(msg.format(_VERSION_FILENAME))

        match = re.match(r'.*?\.dev(?P<dev_num>\d+)', full_v)
        if match is None:
            dev_num = '0'
        else:
            dev_num = match.group('dev_num')
    else:
        git_rev = 'Unknown'
        dev_num = '0'

    if not IS_RELEASED:
        fullversion += '.dev{0}'.format(dev_num)
    else:
        fullversion += "+ansys.ch"

    with open(filename, "wt") as fp:
        fp.write(
            template.format(
                version=VERSION,
                full_version=fullversion,
                git_revision=git_rev,
                is_released=IS_RELEASED))


if __name__ == "__main__":
    write_version_py()
    from envisage import __requires__, __version__

    setup(
        name='envisage',
        version=__version__,
        author="Martin Chilvers, et. al.",
        author_email="info@enthought.com",
        maintainer='ETS Developers',
        maintainer_email='enthought-dev@enthought.com',
        url='http://docs.enthought.com/envisage',
        download_url='https://github.com/enthought/envisage',
        classifiers=[
            c.strip()
            for c in """\
            Development Status :: 5 - Production/Stable
            Intended Audience :: Developers
            Intended Audience :: Science/Research
            License :: OSI Approved :: BSD License
            Operating System :: MacOS
            Operating System :: Microsoft :: Windows
            Operating System :: OS Independent
            Operating System :: POSIX
            Operating System :: Unix
            Programming Language :: Python
            Topic :: Scientific/Engineering
            Topic :: Software Development
            Topic :: Software Development :: Libraries
            """.splitlines() if len(c.strip()) > 0
        ],
        description='extensible application framework',
        long_description=open('README.rst').read(),
        entry_points="""
            [envisage.plugins]
            envisage.core = envisage.core_plugin:CorePlugin
            """,
        ext_modules=[],
        install_requires=__requires__,
        license="BSD",
        packages=find_packages(),
        package_data={
            '': [
                'images/*',
                '*.ini',
            ],
            'envisage.tests': [
                'bad_eggs/*.egg', 'eggs/*.egg', 'plugins/pear/*.py',
                'plugins/banana/*.py', 'plugins/orange/*.py'
            ]
        },
        platforms=["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
        zip_safe=False, )
