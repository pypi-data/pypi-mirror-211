from setuptools import setup, find_packages

with open("../ConfigWizard/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="configwizard",
    version="1.0.5",
    author="Lapis Pheonix",
    description="A package for handling configuration files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LapisPhoenix/ConfigWizard",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11.3",
    install_requires=["tomli_w"],
)