#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(name = 'taskgen',
      version = '0.1.1',
      author = 'Артём Золотаревский',
      author_email = 'artyom@zolotarevskiy.ru',
      description = 'Генератор экзаменационных билетов на базе MikTex',
      long_description = long_description,
      long_description_content_type = "text/markdown",
      url = 'https://github.com/metrazlot/ExamGenerator',
      project_urls = {
            'Bug Tracker': 'https://github.com/metrazlot/ExamGenerator/issues',
      },
      license = 'GPLV3',
      packages = find_packages(),
      install_requires = ['selenium', 'webdriver_manager', 'PyPDF2', 'pylatexenc'],
      classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
      ],
)
