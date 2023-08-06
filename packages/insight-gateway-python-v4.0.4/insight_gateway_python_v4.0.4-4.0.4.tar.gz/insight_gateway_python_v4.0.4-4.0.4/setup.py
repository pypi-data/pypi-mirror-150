from setuptools import find_packages
from setuptools import setup

from setuptools import find_packages
from setuptools import setup

setup(
    name="insight_gateway_python_v4.0.4",
    author="htsc",
    version="4.0.4",
    author_email="insight@htsc.com",
    description="insight_gateway_python_4.0.4",
    long_description="insight_gateway_python_v4.0.4",
    license='insightpythonsdk',
    project_urls={
        'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/pypa/sampleproject/',
        'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },

    #package_dir={'': 'insight_gateway_python_v4.0.0'},
    packages=['insight_gateway_python_v400/com','insight_gateway_python_v400/com/interface','insight_gateway_python_v400/com/libs/python37/x64'],
    data_files= ['insight_gateway_python_v400/com/cert/HTInsightCA.crt','insight_gateway_python_v400/com/cert/InsightClientCert.pem','insight_gateway_python_v400/com/cert/HTISCA.crt','insight_gateway_python_v400/com/cert/InsightClientCert.pem'],
    package_data={'insight_gateway_python_v400.com.libs.python37.x64': ['*.dll','*.pyd']},
    install_requires=['numpy>=1.14'],

    python_requires='>=3.7',
)