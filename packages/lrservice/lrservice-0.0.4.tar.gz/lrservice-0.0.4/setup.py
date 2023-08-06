import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
long_description = "A python package for demonstrating how to make REST API service for linear regression"

setuptools.setup(
    name="lrservice",
    version="0.0.4",
    author="Tyler Tang",
    author_email="tyler.x.tang@outlook.com",
    description="A python package for demonstrating how to make REST API service for linear regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CyberPlayerOne/lrservice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)
