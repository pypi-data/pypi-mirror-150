from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name='detik-scrapper',
    version="1.0.3",
    description='Detik Scrapping',
    long_description=open('README.rst').read(),
    long_description_content_type='text/markdown',
    author='Kiyora',
    author_email='dev@sipaling.top',
    url='https://sipaling.top',
    license='MIT',
    packages=find_packages(),
    classifiers=classifiers,
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    keywords='detik scraping, scrapper',
)
