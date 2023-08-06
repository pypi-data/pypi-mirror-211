from setuptools import setup

setup(
    name='wrapper_secrets_manager',
    version='0.0.1',
    description='This is a custom package to read secrets from GCP.',
    packages=['wrapper_secrets_manager'],
    install_requires=[
        'google_cloud_secret_manager==2.16.1'
    ],
)

