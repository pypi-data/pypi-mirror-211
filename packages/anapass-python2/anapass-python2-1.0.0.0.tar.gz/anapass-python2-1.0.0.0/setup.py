import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anapass-python2", # Replace with your own username
    version="1.0.0.0",
    author="hthwang",
    author_email="hthwang@anapass.com",
    description="Anapass2 Python Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.anapass.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

