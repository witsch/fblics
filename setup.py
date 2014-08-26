from setuptools import setup, find_packages

name = 'fblics'
version = 'v1-dev'

setup(name=name,
    version=version,
    description='convert Frauenbundesliga schedule to iCalendar data exchange format',
    url='https://github.com/witsch/fblics',
    author='Andreas Zeidler',
    author_email='az at zitc.de',
    classifiers=[
        "Programming Language :: Python",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'beautifulsoup4',
        'setuptools',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'fblics = fblics:main',
        ],
    },
)
