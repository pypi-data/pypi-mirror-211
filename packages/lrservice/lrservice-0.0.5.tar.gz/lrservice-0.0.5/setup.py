import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
long_description = "A python package for demonstrating how to make REST API service for linear regression"

setuptools.setup(
    name="lrservice",
    version="0.0.5",
    author="Tyler Tang",
    author_email="tyler.x.tang@outlook.com",
    description="A python package for demonstrating how to make REST API service for linear regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CyberPlayerOne/lrservice",
    packages=setuptools.find_packages(),
    install_requires=[
        'scikit-learn==1.2.2',
        'matplotlib==3.7.1',
        'numpy==1.24.3',
        'flask==2.2.2',
        'gunicorn==20.1.0',
        'dill==0.3.6'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)
