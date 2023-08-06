from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pytest"]

setup(
    name="python_round",
    version="0.0.2",
    author="Abd Alrahman Hajjar",
    author_email="Abdalrahman.hajjar@lavita.de",
    description="A package to to round Float numbers.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/AbdHajjar/python_round",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
    ],
)