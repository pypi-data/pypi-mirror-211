import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="needl",
    version="0.0.6",
    author="Klaudia Adamowicz",

    author_email='klaudia.adamowicz@uni-hamburg.de',
    url='http://pypi.python.org/pypi/needl/',
    license='LICENSE',
    description="Python Package to access Epistasis Disease Atlas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['needl', 'needl.objects'],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Science/Research',
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',
    install_requires=[
        "pandas>=1.2.0",
        "requests",
    ]
)
