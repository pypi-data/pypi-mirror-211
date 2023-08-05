from setuptools import setup, find_packages
setup(
    name='my-provider',
    version='0.1.9',
    packages=find_packages(),
    install_requires=[
        'apache-airflow>=2.0.0',
        'tencentcloud-sdk-python>=3.0.901'

    ],
    entry_points={
        'apache_airflow_provider': [
            'provider_info=my_provider.__init__:get_provider_info'
        ]
    }
)