import setuptools

with open("README.md", "rt") as f:
    long_description = f.read()

setuptools.setup(
    name="eset",
    version="0.0.2",
    author="Frey Waid",
    author_email="logophage1@gmail.com",
    description="Extended set",
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/freywaid/eset",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
