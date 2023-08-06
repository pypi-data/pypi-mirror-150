import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="thwAPI",
    version="1.1.0",
    description="Keeping Tabs With The Hashnode Writeathon (THW)",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords='Hashnode Writeathon Challenges Blogging Tech',
    url="https://github.com/Ronlin1/THW",
    author="Ronnie Atuhaire",
    author_email="ronlinx6@gmail.com",
    license="MIT",
    install_requires=[
          'requests',
          'progress'
      ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["thwAPI"],
    include_package_data=True,
    package_dir={'/':'thwAPI'}
)