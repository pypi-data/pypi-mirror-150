import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subfinder-vvvin",
    version="1.0.4",
    author="mian",
    author_email="wukuizongvincent@gmail.com",
    include_package_data=True,
    description="A Address Finder",
    install_requires=[
        "textdistance"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'subfinder': ['suburbs.dat', 'suburbgeo.dat']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
