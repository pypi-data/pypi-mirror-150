import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # pip3 1000pip Climber System download
    name="1000pip Climber System download", 
    version="2022",
    author="1000pip Climber System download",
    author_email="1000pip@ClimberSystemdownload.com",
    description="1000pip Climber System download",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://156544mlxov28levev7grc9v9g.hop.clickbank.net/?tid=py",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
