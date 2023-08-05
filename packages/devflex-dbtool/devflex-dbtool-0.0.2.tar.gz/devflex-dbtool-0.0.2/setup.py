import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="devflex-dbtool", # Replace with your own username
    version="0.0.2",
    author="DevFlex",
    author_email="workall350@gmail.com",
    description="my ezdb tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OverMony/python-devflex-dbtool-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ['numpy'],
    python_requires='>=3.6',
)