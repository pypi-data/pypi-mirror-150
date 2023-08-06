# python setup.py --dry-run --verbose install

from distutils.core import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='pyNetatmoHue',
    version='0.0.5',
    classifiers=[        
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
        ],
    author='Steve de Peijper',
    author_email='steve.depeijper@gmail.com',
    py_modules=['pyNetatmoHue'],
    scripts=[],
    install_requires=['python-dateutil',
      ],
    data_files=[],
    url='https://github.com/stevedep/Netatmo_PPM_Hue',    
    license='GPL V3',
    description='Simple API to access Netatmo weather station data from any python script.',
    long_description=long_description
)
