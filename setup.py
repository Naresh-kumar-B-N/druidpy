import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="druidpy",
    version="1.0.2.2",
    author="Naresh Kumar B N",
    author_email="nareshbn007@gmail.com",
    description="A package which provides minimum required methods for working with Druid through Python!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Naresh-kumar-B-N/druidpy/archive/v1.0.2.2.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
