import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aich",
    version="0.0.5",
    author="Arijit Aich",
    author_email="a2.arijitaich@gmail.com",
    description="Encrypt Words From Any Language. Get Token In Hindi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arijitaich/AICH-Encryption",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)