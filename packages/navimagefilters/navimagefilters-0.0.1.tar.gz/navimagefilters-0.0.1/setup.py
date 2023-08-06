import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="navimagefilters", # Replace with your own username for package
    version="0.0.1",
    author="Navaneeth", #Replace with your own name
    author_email="navaneethsharma2310oct@gmail.com", #Replace with your own email
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Navaneeth-Sharma/imagefilters/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)