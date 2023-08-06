from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="convappro",
    version="0.0.1",
    author="Marion NOVERRAZ, Mostafa HAGHVIRDILOO, Alexandre RAMDOO, Henri MACEDO GONCALVES",
    author_email="henri.macedo-goncalves@etu.unistra.fr",
    description="Projet d'analyse: Sujet 31",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/henrimacedo/convappro.git",
    project_urls={
        "Bug Tracker": "https://github.com/henrimacedo/convappro.git/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",
)
