from setuptools import find_packages
from setuptools import setup

setup(
    name="insight_gateway_python",
    author="htsc",
    version="4.0.7",
    author_email="insight@htsc.com",
    description="insight_gateway_python",
    long_description="insight_gateway_python",
    license='insightpythonsdk',
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/pypa/sampleproject/',
        'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },


    packages= ['com'],
    include_package_data=True,
    install_requires=[],

    python_requires='>=3.7.*',
)