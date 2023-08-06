import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy-yt-dlp-py",                     # This is the name of the package
    version="1.0.0",                        # The initial release version
    author="Yarrtt",                     # Full name of the author
    description="Easier yt-dlp download using in python",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=2.6.6',              # Minimum version requirement of the package
    py_modules=["ytdlpy"],             # Name of the python package
    package_dir={'':'ytdlpy/src'},     # Directory of the source code of the package
    install_requires=[""]                     # Install other dependencies if any
)