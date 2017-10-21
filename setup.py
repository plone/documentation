# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='plone.documentation',
    version='dev',
    description='Plone Documentation',
    long_description=open("README.rst").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Framework :: Sphinx',
        'License :: OSI Approved :: Creative Commons Attribution 4.0 International license (CC BY 4.0)',  # NOQA: E501
        'Topic :: Software Development :: Documentation',
        'Intended Audience :: Developers',
    ],
    keywords='plone documentation',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://github.com/plone/documentation.git',
    license='GPL',
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    extras_require={
    },
    entry_points="""
    # -*- Entry points: -*-
    """,
)
