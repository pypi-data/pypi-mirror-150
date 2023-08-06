from pathlib import Path
from setuptools import find_packages, setup
dependencies = ['tkinter', 'sqlite3', 'tkcalendar', 'functools', 'collections', 'itertools', 'operator','mako','datetime','calendar','contextlib', 'os','re']
# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='fanompo',
    packages=find_packages('src',exclude=['tests']),
    version='0.0.1',
    description='Propensity score matching for python and graphical plots',
    author='Author name here',
author_email='author@example.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/",
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
    #setup_requires=['pytest-runner'],
    #tests_require=['pytest==4.4.1'],
##    test_suite='tests',
)
