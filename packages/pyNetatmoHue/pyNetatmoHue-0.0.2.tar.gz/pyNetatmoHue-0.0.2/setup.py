# python setup.py --dry-run --verbose install

from distutils.core import setup

setup(
    name='pyNetatmoHue',
    version='0.0.2',
    classifiers=[        
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
        ],
    author='Steve de Peijper',
    author_email='steve.depeijper@gmail.com',
    py_modules=['pynetatmohue'],
    scripts=[],
    data_files=[],
    url='https://github.com/philippelt/netatmo-api-python',
    download_url='https://github.com/philippelt/netatmo-api-python/archive/v2.1.0.tar.gz',
    license='GPL V3',
    description='Simple API to access Netatmo weather station data from any python script.'
)
