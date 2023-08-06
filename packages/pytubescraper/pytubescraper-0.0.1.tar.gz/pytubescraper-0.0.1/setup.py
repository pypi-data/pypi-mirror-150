from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A python package that can scrape youtube'
LONG_DESCRIPTION = '''This libary has functions like titles(youtube_id,results_number)
, ids(title,results,number) and recommandations(title). It should be used for youtube webbscraping'''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pytubescraper",
        version=VERSION,
        author="Aarav",
        author_email="aarav.trivedi12@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['urllib.request','requests','py_youtube'], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['youtube', 'scrapers'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)
