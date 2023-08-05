
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="generate-invitation-codes",
    version="1.0.0",
    packages=find_packages(),
    py_modules=['generate_invitation_codes'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'generate_invitation_codes = generate_invitation_codes:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
