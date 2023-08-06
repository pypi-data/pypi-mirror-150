import setuptools
#Basic setup.py for package instalation
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="locass",
    version="1.0.4",
    author="NightlyShelf",
    description="Simple localization manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    py_modules=["locass"],
    package_dir={'':'locass/src'},
    install_requires=[]
)