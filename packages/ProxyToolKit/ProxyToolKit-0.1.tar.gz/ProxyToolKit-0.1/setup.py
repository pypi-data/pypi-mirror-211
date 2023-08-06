from setuptools import setup, find_packages

setup(
    name='ProxyToolKit',
    version='0.1',
    license='MIT',
    author='Coding With Devil',
    author_email='codingwithdevil@gmail.com',
    description='Proxy Scraper and Checker',
    long_description='''With this module you can easly scrape and check proxy without any limitations ,also you can use this to webapps ''',
    long_description_content_type='text/markdown',
    url='https://github.com/codingwithdevil/ProxyToolKit.git',
    download_url='https://github.com/codingwithdevil/ProxyToolKit/archive/refs/tags/v0.1.tar.gz',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'beautifulsoup4',
        'bs4',
        'certifi',
        'charset-normalizer',
        'idna',
        'PyQt5',
        'PyQt5-Qt5',
        'PyQt5-sip',
        'requests',
        'soupsieve',
        'urllib3',
        # List other dependencies required by your package
    ],
    python_requires='>=3.7',
)
