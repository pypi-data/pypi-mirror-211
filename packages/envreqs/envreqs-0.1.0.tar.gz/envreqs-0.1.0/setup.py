from setuptools import setup
from envreqs import __version__

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='envreqs',
    version=__version__,
    description='An env builder for Python project',
    url='https://github.com/santhu2210/envbuilder',
    author='Shantha Kumar',
    author_email='msgshanth@gmail.com',
    license='GNU GENERAL PUBLIC LICENSE',
    packages=['envreqs'],
    install_requires=['docopt'],
    long_description = readme + '\n',
    long_description_content_type='text/x-rst',
    entry_points={
        'console_scripts': [
            'envreqs=envreqs.envreqs:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10'
    ],
)