from setuptools import find_packages
from setuptools import setup

setup(
    name="insight_gateway_python_v4.0.3",
    author="htsc",
    version="4.0.3",
    author_email="insight@htsc.com",
    description="insight_gateway_python_4.0.3",
    long_description="insight_gateway_python_v4.0.3",
    license='insightpythonsdk',
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/pypa/sampleproject/',
        'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },

    package_dir={'': 'insight_gateway_python_v4.0.0'},
    packages=find_packages('insight_gateway_python_v4.0.0'),
    #packages=['com','com/interface','com/libs/python37/x64'],
    data_files={'': ['com/cert/*.crt','com/cert/*.pem']},
    package_data={'': ['com/libs/python37/x64/*.dll','com/libs/python37/x64/*.pyd']},
    install_requires=['numpy>=1.14'],

    python_requires='>=3.7',
)