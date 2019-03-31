import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysykkel",
    version="0.1",
    author="Tore Sinding Bekkedal",
    author_email="toresbe@gmail.com",
    description="Python library for GBFS / Oslo Bysykkel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toresbe/pysykkel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
)
