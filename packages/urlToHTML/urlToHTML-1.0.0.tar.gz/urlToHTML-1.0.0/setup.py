import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="urlToHTML",
    version="1.0.0",
    description="Auto save HTML files from URLs for Offline Viewing",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords='HTML URLS Save Chrome Offline',
    url="https://github.com/Ronlin1/urlToHTML",
    author="Ronnie Atuhaire",
    author_email="ronlinx6@gmail.com",
    license="MIT",
    install_requires=[
          'requests',
      ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["urlToHTML"],
    include_package_data=True,
    package_dir={'/':'urlToHTML'}
)