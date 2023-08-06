from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Roboto SDK'
LONG_DESCRIPTION = 'Coming soon'

setup(
    name="roboto-sdk",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Roboto",
    author_email="admin@roboto.ai",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
