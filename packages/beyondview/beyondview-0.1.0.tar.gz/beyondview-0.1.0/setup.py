import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beyondview",
    version="0.1.0",
    author="Jesson Go",
    author_email="jesson.go@beyondview.com",
    description="General python tools for beyondview",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jgbv/beyondview",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)