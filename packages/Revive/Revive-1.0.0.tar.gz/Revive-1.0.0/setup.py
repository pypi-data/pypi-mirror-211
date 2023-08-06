from setuptools import setup, find_packages

setup(
    name='Revive',
    version='1.0.0',
    description='A Cool Revive tool',
    author='The Revive Team',
    packages=find_packages(),
    install_requires=[
        'click'
    ],
    entry_points={
        'console_scripts': [
            'revive=revive.cli:revive'
        ]
    }
)