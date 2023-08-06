from setuptools import setup, find_packages

setup(
    name='chater',
    version='1.0.1',
    packages=find_packages(include=['chater']),
    author='Sricor',
    author_email='josricor@outlook.com',
    description='Using ChatGPT in Python',
    long_description='foo',
    license='MIT',
    install_requires=[
        'requests',
        'pydantic'
    ]
)
