"""Convert MEDM's .adl files to PyDM's .ui format."""

__project__ = u"adl2pydm"
__description__ = __doc__
__copyright__ = u"2017-2021, UChicago Argonne, LLC"
__authors__ = [
    u"Pete Jemian",
]
__author__ = ", ".join(__authors__)
__institution__ = u"Advanced Photon Source, Argonne National Laboratory"
__author_email__ = u"jemian@anl.gov"
__url__ = u"https://github.com/BCDA-APS/adl2pydm"
__license__ = u"(c) " + __copyright__
__license__ += u" (see LICENSE.txt file for details)"
__platforms__ = "any"
__zip_safe__ = False
__exclude_project_dirs__ = "adl2pydm/tests tests conda-recipe build".split()
__python_version_required__ = ">=3.7"

__package_name__ = __project__
__long_description__ = __description__

__install_requires__ = []  # no requirements, only standard libraries

__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: Freely Distributable",
    "License :: Public Domain",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Astronomy",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Chemistry",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Software Development :: Embedded Systems",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Software Development",
    "Topic :: Utilities",
]

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
