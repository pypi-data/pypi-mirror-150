import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiplusiot",                     # This is the name of the package
    version="1.0.0",                        # The initial release version
    author="aiplus",                     # Full name of the author
    authore_email='aipluseu@gmail.com',
    description="aiPlus IOT library",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    repository_url="https://github.com/GII/aiplus-iot",
    #packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["aiplusiot"],             # Name of the python package
    packages=setuptools.find_packages('src'),
    package_dir={'':'src'},     # Directory of the source code of the package
    #packages=setuptools.find_packages(include=['.*']),
    install_requires=['hass-client']                     # Install other dependencies if any
)