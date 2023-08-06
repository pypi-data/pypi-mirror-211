import os
import setuptools

# pip install ./PyORM --upgrade -t /home/jam/.local/lib/python3.10/site-packages/PyORM

readme = open("%s%sREADME.md"%(os.path.dirname(__file__), os.path.sep)).read()


setuptools.setup(
    name='PyCyphORM',
    version='0.1.3',
    author='jafrmartins',
    keywords='sqlite encrypted inmemory orm',
    author_email='j.afr.martins@outlook.pt',
    description='A Minimalistic SQLite InMemory Encrypted ORM',
    packages=setuptools.find_packages('src'),
    install_requires=[],
    package_dir={'PyCyphORM': 'src/PyCyphORM', },
    entry_points={
        'console_scripts': [
            'pycyphorm=cli:cli',
        ],
    },
    include_package_data=True,
    long_description=readme,
    long_description_content_type='text/markdown'
)