from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'With just one click "martscraper" felicitates product query based scrapping of listed products on Amazon and Flipkart. '

# Setting up
setup(
    name="martscraper",
    version=VERSION,
    author="Shreyansh Padarha",
    author_email="<shreyansh.padarha@hotmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[    'beautifulsoup4',
    'Flask',
    'ipython',
    'matplotlib',
    'nltk',
    'numpy',
    'numpy',
    'pandas',
    'plotly',
    'regex',
    'Requests',
    'scipy',
    'seaborn',
    'tabulate',
    'tqdm',
    'transformers',
    'wordcloud'],
    keywords=['python', 'machine learning',
               'webscrapping', 'Amazon', 'Flipkart', 
               'ecommerce','products','nlp','sentiment analysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS"
    ]
)