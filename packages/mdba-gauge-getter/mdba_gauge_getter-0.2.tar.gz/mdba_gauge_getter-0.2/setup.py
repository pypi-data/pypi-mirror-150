import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='mdba_gauge_getter',
    version='0.2',
    author='Murray Darling Basin Authority',
    author_email='Ben.Bradshaw@mdba.gov.au', 
    description='Facilitates waterflow gauge data ingest from several endpoints. Dependency to several other projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MDBAuth/MDBA_Gauge_Getter',
    project_urls={
        'Bug Tracker': 'https://github.com/MDBAuth/MDBA_Gauge_Getter/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    packages=['mdba_gauge_getter',],
    package_data={'': ['data/*.csv']},
    python_requires='>=3.6',
)

