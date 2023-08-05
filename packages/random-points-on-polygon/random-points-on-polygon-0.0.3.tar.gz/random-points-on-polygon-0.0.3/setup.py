import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="random-points-on-polygon",
    version="0.0.3",
    author="Mauro Saladino",
    author_email="maurosaladino7@gmail.com",
    url="https://github.com/maurosaladino/random-points-on-polygon",
    description="A simple Python library based on Shapely to generate random points on Polygon or MultiPolygon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=requirements,
)
