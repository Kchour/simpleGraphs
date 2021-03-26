import setuptools

# ADD URL, long_description, version!

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpleGraphM", # Replace with your own username
    version="0.0.1",
    author="Kenny Chour",
    author_email="chour.kenny@yahoo.com",
    description="Simple graph implementation and collection of algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
