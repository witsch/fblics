from setuptools import setup

name = 'fblics'
version = 'v1'

setup(name=name,
    version=version,
    description='convert Frauen-Bundesliga schedule to iCalendar data exchange format',
    url='https://github.com/witsch/fblics',
    author='Andreas Zeidler',
    author_email='az at zitc.de',
    classifiers=[
        "Programming Language :: Python",
    ],
    py_modules=['fblics'],
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
