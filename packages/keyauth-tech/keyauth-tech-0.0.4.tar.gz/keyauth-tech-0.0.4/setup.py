from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Operating System :: OS Independent',
]

setup(
    name='keyauth-tech',
    version='0.0.4',
    description='Authentication Tool for Authenticating Users, HWIDs and Licenses to keep your Code secure from malicious activities.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://keyauth.tech',
    author='Collin Stokes',
    author_email='rehan009a@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='authentication, auth, keys, hwid',
    packages=find_packages(),
    install_requires=['requests', 'colorama']
)
